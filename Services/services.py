'''
import requests
import config
from app import db, app
from DataLayer.Models.models import WeatherStationData, WeatherForecastData
import json
from datetime import datetime
from flask import jsonify

from DataLayer.WeatherPredictionRepository import add_forecast_data,commit_changes


def fetch_weather_forecast(date):
    with app.app_context():
        try:
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
                        precipitation_mm=data['daily']['precipitation_sum'][i],
                        fetched_at=datetime.now()
                    )
                    #db.session.add(forecast_data)
                    add_forecast_data(forecast_data)
            #db.session.commit()
            commit_changes()
            print(datetime.now().strftime('%d-%m %H:%M') + " Forecast fetch successful, data saved.")

        except requests.RequestException as e:
            print(f"Request failed: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


def fetch_weather_forecast_range(start_date, end_date):
    with app.app_context():
        response = requests.get(config.weather_forecast_url)
        response.raise_for_status()
        data = response.json()

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
                        precipitation_mm=precipitation_mm,
                        fetched_at=datetime.now()
                    )
                    db.session.add(forecast_data)

            db.session.commit()
            print(datetime.now().strftime('%d-%m %H:%M') + " Range forecast fetch successful, data saved.")

        else:
            print("Date range not found in the data.")


def fetch_and_process_data():
    with app.app_context():
        headers = {
            'Authorization': f'Bearer {config.weatherstation_access_key}'
        }
        response = requests.get(config.weatherstation_device_url, headers=headers)
        if response.status_code == 200:
            print(datetime.now().strftime('%d-%m %H:%M') + " Station fetch successful, saving...")
            handle_partial_json(response.text)
            return {'message': "Data fetched and saved successfully", 'code': 200}
        else:
            error_message = f"Failed to retrieve data with status code {response.status_code}"
            print(error_message)
            print(response.text)
            return {'message': error_message, 'code': response.status_code}


def get_weather_forecast_by_date(date):
    with app.app_context():
        forecast_data = WeatherForecastData.query.filter_by(date=date).first()
        if forecast_data:
            return jsonify({
                'date': forecast_data.date.strftime('%Y-%m-%d'),
                'max_temperature': forecast_data.max_temperature,
                'min_temperature': forecast_data.min_temperature,
                'sunshine_duration_minutes': forecast_data.sunshine_duration_minutes,
                'precipitation_mm': forecast_data.precipitation_mm
            })
        else:
            return jsonify({'error': 'No forecast data available for this date'}), 404

#in repo ??
def handle_partial_json(text):
    with app.app_context():
        index = text.rfind('{"result"')
        data = json.loads(text[index:])
        messages = data['result']['uplink_message']['decoded_payload']['messages']
        received_at = data['result']['received_at']
        fetched_at = datetime.now()

        for message in messages:
            weather_data = WeatherStationData(
                measurement_value=message['measurementValue'],
                measurement_type=message['type'],
                received_at=received_at,
                fetched_at=fetched_at
            )
            db.session.add(weather_data)
        db.session.commit()
'''