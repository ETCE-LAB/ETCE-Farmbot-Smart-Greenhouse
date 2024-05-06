from flask import Flask
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
import json
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import config

app = Flask(__name__)
api = Api(app, version='2.0', title='FarmBot API',
          description='Different endpoints for the FarmBot, SmartGreenhouse and Weather Station')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class WeatherStationData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    measurement_value = db.Column(db.Float, nullable=False)
    measurement_type = db.Column(db.String(50), nullable=False)
    received_at = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<WeatherStationData {self.measurement_type} {self.received_at}>"


class WeatherForecastData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(120), nullable=False)
    max_temperature = db.Column(db.Float)
    min_temperature = db.Column(db.Float)
    sunshine_duration_minutes = db.Column(db.Integer)
    precipitation_mm = db.Column(db.Float)

    def __repr__(self):
        return f"<WeatherForecastData {self.date}>"


def create_tables():
    with app.app_context():
        db.create_all()


# Namespace for Weather Station and Forecast
ns = api.namespace('weatherstation', description='Endpoints for the Weather Station')
forecast_ns = api.namespace('forecast', description='Endpoints for Weather Forecast')


@ns.route('/data')
class Data(Resource):
    def get(self):
        with app.app_context():
            data = WeatherStationData.query.all()
            if data:
                return [{'measurement_value': item.measurement_value, 'measurement_type': item.measurement_type,
                         'received_at': item.received_at} for item in data], 200
            else:
                api.abort(404, 'Data not found')


@ns.route('/fetch')
class Fetch(Resource):
    def get(self):
        fetch_and_process_data()
        return {'status': 'fetched data successfully'}, 200


@forecast_ns.route('/get/<date>')
class Forecast(Resource):
    def get(self, date):
        with app.app_context():
            forecast_data = WeatherForecastData.query.filter_by(date=date).first()
            if forecast_data:
                return {col.name: getattr(forecast_data, col.name) for col in forecast_data.__table__.columns}, 200
            else:
                forecast_data = fetch_weather_forecast(date)
                return forecast_data, 200


@forecast_ns.route('/range/<start_date>/<end_date>')
class ForecastRange(Resource):
    @api.doc(description='Retrieve the weather forecast for a range of dates.',
             params={'start_date': 'The start date of the forecast range (format YYYY-MM-DD)',
                     'end_date': 'The end date of the forecast range (format YYYY-MM-DD)'},
             responses={200: 'Success', 400: 'Bad Request', 404: 'No data found for the specified range',
                        500: 'Internal Server Error'})
    def get(self, start_date, end_date):
        try:
            forecast_data = fetch_weather_forecast_range(start_date, end_date)
            if forecast_data:
                return forecast_data, 200
            else:
                api.abort(404, 'No data found for the specified range')
        except requests.exceptions.RequestException as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, str(e))


def fetch_weather_forecast_range(start_date, end_date):
    with app.app_context():
        response = requests.get(config.weather_forecast_url)
        response.raise_for_status()
        data = response.json()
        forecast_list = []
        start_index = next((i for i, date in enumerate(data['daily']['time']) if date == start_date), None)
        end_index = next((i for i, date in enumerate(data['daily']['time']) if date == end_date), None)

        if start_index is not None and end_index is not None and start_index <= end_index:
            for i in range(start_index, end_index + 1):
                date = data['daily']['time'][i]
                max_temperature = data['daily']['temperature_2m_max'][i]
                min_temperature = data['daily']['temperature_2m_min'][i]
                sunshine_duration_minutes = int(data['daily']['sunshine_duration'][i] / 60)
                precipitation_mm = data['daily']['precipitation_sum'][i]

                forecast_data = WeatherForecastData.query.filter_by(date=date).first()
                if forecast_data:
                    forecast_data.max_temperature = max_temperature
                    forecast_data.min_temperature = min_temperature
                    forecast_data.sunshine_duration_minutes = sunshine_duration_minutes
                    forecast_data.precipitation_mm = precipitation_mm
                else:
                    forecast_data = WeatherForecastData(
                        date=date,
                        max_temperature=max_temperature,
                        min_temperature=min_temperature,
                        sunshine_duration_minutes=sunshine_duration_minutes,
                        precipitation_mm=precipitation_mm
                    )
                    db.session.add(forecast_data)

                forecast_list.append({
                    'date': date,
                    'max_temperature': max_temperature,
                    'min_temperature': min_temperature,
                    'sunshine_duration_minutes': sunshine_duration_minutes,
                    'precipitation_mm': precipitation_mm
                })
            db.session.commit()
            print(datetime.datetime.now().strftime('%d-%m %H:%M') + " Range forecast fetch successful, saving...")
            return forecast_list
    return None


def fetch_and_process_data():
    with app.app_context():
        print(f"Fetching data at {datetime.datetime.now().strftime('%m-%d %H:%M')}")
        headers = {
            'Authorization': f'Bearer {config.weatherstation_access_key}',
            'Accept': 'application/json'
        }
        response = requests.get(config.weatherstation_device_url, headers=headers)
        if response.status_code == 200:
            print(datetime.datetime.now().strftime('%d-%m %H:%M') + " Station data retrieval successful, saving...")
            handle_partial_json(response.text)
        else:
            print("Failed to retrieve data:", response.status_code, response.text)


def handle_partial_json(text):
    with app.app_context():
        try:
            index = text.rfind('{"result"')
            data = json.loads(text[index:])
            messages = data['result']['uplink_message']['decoded_payload']['messages']
            received_at = data['result']['received_at']
            for message in messages:
                weather_data = WeatherStationData(
                    measurement_value=message['measurementValue'],
                    measurement_type=message['type'],
                    received_at=received_at
                )
                db.session.add(weather_data)
            db.session.commit()
        except Exception as e:
            pass


def fetch_weather_forecast(date):
    with app.app_context():
        response = requests.get(config.weather_forecast_url)
        response.raise_for_status()
        data = response.json()
        for i, day in enumerate(data['daily']['time']):
            if day == date:
                sunshine_duration_minutes = int(data['daily']['sunshine_duration'][i] / 60)
                forecast_data = WeatherForecastData(
                    date=day,
                    max_temperature=data['daily']['temperature_2m_max'][i],
                    min_temperature=data['daily']['temperature_2m_min'][i],
                    sunshine_duration_minutes=sunshine_duration_minutes,
                    precipitation_mm=data['daily']['precipitation_sum'][i]
                )
                db.session.add(forecast_data)
                db.session.commit()
                print(datetime.datetime.now().strftime('%d-%m %H:%M') + " Forecast fetch successful, saving...")
                return {
                    'date': day,
                    'max_temperature': data['daily']['temperature_2m_max'][i],
                    'min_temperature': data['daily']['temperature_2m_min'][i],
                    'sunshine_duration_minutes': sunshine_duration_minutes,
                    'precipitation_mm': data['daily']['precipitation_sum'][i]
                }
        return None


scheduler = BackgroundScheduler()
# Fetch station data every 15 minutes
scheduler.add_job(fetch_and_process_data, 'interval', minutes=15)
# Fetch forecast for the next day every 12 hours
scheduler.add_job(fetch_weather_forecast, 'interval', hours=12,
                  args=[(datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')])
# Fetch forecast for the next week every 12 hours
scheduler.add_job(fetch_weather_forecast_range, 'interval', hours=12,
                  args=[(datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
                        (datetime.datetime.now() + datetime.timedelta(days=7)).strftime('%Y-%m-%d')])
scheduler.start()

if __name__ == '__main__':
    create_tables()
    try:
        app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler shut down successfully!")
