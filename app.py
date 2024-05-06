from flask import Flask
from flask_restx import Api, Resource, fields
import json
import requests
import csv
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import config
import os

app = Flask(__name__)
api = Api(app, version='2.0', title='FarmBot API',
          description='Different endpoints for the FarmBot, SmartGreenhouse and Weather Station')

# Swagger data model definition for API documentation
message_model = api.model('WeatherData', {
    'Date': fields.String(required=True, description='The date of the weather data', example="2024-05-03"),
    'Temperature Max': fields.Float(required=False, description='Maximum temperature (°C) for the day, forecasted or observed', example=25.0),
    'Temperature Min': fields.Float(required=False, description='Minimum temperature (°C) for the day, forecasted or observed', example=15.0),
    'Current Temperature': fields.Float(required=False, description='Current temperature (°C) at the time of measurement', example=20.0),
    'Humidity': fields.Float(required=False, description='Humidity percentage', example=80.0),
    'Precipitation': fields.Float(required=False, description='Precipitation amount (mm)', example=2.0),
    'Sunshine Duration': fields.Float(required=False, description='Duration of sunshine in minutes', example=50),
    'Wind Speed': fields.Float(required=False, description='Wind speed (km/h)', example=10),
    'Received At': fields.String(required=True, description='Date and time of measurement reception or forecast generation', example="2024-05-03T07:31:56.350079173Z"),
    'Description': fields.String(required=False, description='Weather description', example="Partly cloudy")
})

# Namespace for Weather Station
ns = api.namespace('weatherstation', description='Endpoints for the Weather Station')

# Namespace for Forecast
forecast_ns = api.namespace('forecast', description='Endpoints for Weather Forecast')


@ns.route('/data')
class Data(Resource):
    @api.doc(description='Retrieve all stored weather data in JSON format.',
             responses={200: 'Success', 404: 'File Not Found', 500: 'Internal Server Error'})
    @api.marshal_list_with(message_model)
    def get(self):
        try:
            data = csv_to_json('weather_data.csv')
            return data, 200
        except FileNotFoundError:
            api.abort(404, 'File not found')
        except Exception as e:
            api.abort(500, str(e))


@ns.route('/fetch')
class Fetch(Resource):
    @api.doc(description='Manually trigger the fetching of weather data from TheThingsNetwork.',
             responses={200: 'Data Fetched Successfully'})
    def get(self):
        fetch_and_process_data()
        return {'status': 'fetched data successfully'}, 200


@forecast_ns.route('/get/<date>')
class Forecast(Resource):
    @api.doc(description='Retrieve the weather forecast for a specific date.',
             params={'date': 'The date to retrieve the forecast for (format YYYY-MM-DD)'},
             responses={200: 'Success', 400: 'Bad Request', 404: 'Date not found', 500: 'Internal Server Error'})
    def get(self, date):
        try:
            forecast_data = fetch_weather_forecast(date)
            if forecast_data:
                return forecast_data, 200
            else:
                api.abort(404, 'Date not found in forecast data')
        except requests.exceptions.RequestException as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, str(e))


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
    response = requests.get(config.weather_forecast_url)  # Make sure your API can handle range queries
    response.raise_for_status()
    data = response.json()
    forecast_list = []
    # Assume data['daily']['time'] contains dates in 'YYYY-MM-DD' format
    start_index = next((i for i, date in enumerate(data['daily']['time']) if date == start_date), None)
    end_index = next((i for i, date in enumerate(data['daily']['time']) if date == end_date), None)

    if start_index is not None and end_index is not None and start_index <= end_index:
        for i in range(start_index, end_index + 1):
            sunshine_duration_minutes = int(data['daily']['sunshine_duration'][i] / 60)
            forecast_list.append({
                'date': data['daily']['time'][i],
                'max_temperature': data['daily']['temperature_2m_max'][i],
                'min_temperature': data['daily']['temperature_2m_min'][i],
                'sunshine_duration_minutes': sunshine_duration_minutes,
                'precipitation_mm': data['daily']['precipitation_sum'][i]
            })
        return forecast_list
    return None


def fetch_weather_forecast(date):
    response = requests.get(config.weather_forecast_url)
    response.raise_for_status()
    data = response.json()
    for i, day in enumerate(data['daily']['time']):
        if day == date:
            sunshine_duration_minutes = int(data['daily']['sunshine_duration'][i] / 60)
            return {
                'date': day,
                'max_temperature': data['daily']['temperature_2m_max'][i],
                'min_temperature': data['daily']['temperature_2m_min'][i],
                'sunshine_duration_minutes': sunshine_duration_minutes,
                'precipitation_mm': data['daily']['precipitation_sum'][i]
            }
    return None




def fetch_and_process_data():
    print(f"Fetching data at {datetime.datetime.now().strftime('%m-%d %H:%M')}")
    headers = {
        'Authorization': f'Bearer {config.weatherstation_access_key}',
        'Accept': 'application/json'
    }
    response = requests.get(config.weatherstation_device_url, headers=headers)
    if response.status_code == 200:
        print(datetime.datetime.now().strftime('%d-%m %H:%M') + " Data retrieval successful, saving...")
        handle_partial_json(response.text)
    else:
        print("Failed to retrieve data:", response.status_code, response.text)


def handle_partial_json(text):
    try:
        index = text.rfind('{"result"')
        data = json.loads(text[index:])
        messages = data['result']['uplink_message']['decoded_payload']['messages']
        received_at = data['result']['received_at']
        with open('weather_data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            for message in messages:
                writer.writerow([message['measurementValue'], message['type'], received_at])
    except Exception as e:
        print("Failed to parse truncated JSON:", str(e))


def csv_to_json(filename):
    data = []
    with open(filename, mode='r', newline='') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data


scheduler = BackgroundScheduler()
scheduler.add_job(fetch_and_process_data, 'interval', minutes=15)  # Fetch data every 15 minutes
scheduler.start()

# Initialize CSV file on application startup
if not os.path.exists('weather_data.csv'):
    with open('weather_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Measurement Value', 'Type', 'Received At'])

if __name__ == '__main__':
    try:
        app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler shut down successfully!")
