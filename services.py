import requests
import config
from flask import current_app as app
from app import db
from models import WeatherStationData, WeatherForecastData
import json
import datetime


def fetch_weather_forecast(date):
    try:
        with app.app_context():
            response = requests.get(config.weather_forecast_url)
            response.raise_for_status()
            data = response.json()

            fetched = False
            for i, day in enumerate(data['daily']['time']):
                if day == date:
                    forecast_data = WeatherForecastData(
                        date=day,
                        max_temperature=data['daily']['temperature_2m_max'][i],
                        min_temperature=data['daily']['temperature_2m_min'][i],
                        sunshine_duration_minutes=int(data['daily']['sunshine_duration'][i] / 60),
                        precipitation_mm=data['daily']['precipitation_sum'][i],
                        fetched_at=datetime.datetime.now()
                    )
                    db.session.add(forecast_data)
                    db.session.commit()
                    fetched = True
                    break

            if fetched:
                return {
                    'date': day,
                    'max_temperature': data['daily']['temperature_2m_max'][i],
                    'min_temperature': data['daily']['temperature_2m_min'][i],
                    'sunshine_duration_minutes': int(data['daily']['sunshine_duration'][i] / 60),
                    'precipitation_mm': data['daily']['precipitation_sum'][i]
                }
            return None
    except requests.RequestException as e:
        app.logger.error(f"Failed to fetch data: {str(e)}")
        return None


def fetch_weather_forecast_range(start_date, end_date):
    try:
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
                    forecast_data = WeatherForecastData(
                        date=date,
                        max_temperature=data['daily']['temperature_2m_max'][i],
                        min_temperature=data['daily']['temperature_2m_min'][i],
                        sunshine_duration_minutes=int(data['daily']['sunshine_duration'][i] / 60),
                        precipitation_mm=data['daily']['precipitation_sum'][i],
                        fetched_at=datetime.datetime.now()
                    )
                    db.session.add(forecast_data)
                    forecast_list.append({
                        'date': date,
                        'max_temperature': data['daily']['temperature_2m_max'][i],
                        'min_temperature': data['daily']['temperature_2m_min'][i],
                        'sunshine_duration_minutes': int(data['daily']['sunshine_duration'][i] / 60),
                        'precipitation_mm': data['daily']['precipitation_sum'][i]
                    })
                db.session.commit()
                return forecast_list
            return None
    except requests.RequestException as e:
        app.logger.error(f"Failed to fetch range data: {str(e)}")
        return None


def fetch_and_process_data():
    try:
        with app.app_context():
            headers = {'Authorization': f'Bearer {config.weatherstation_access_key}'}
            response = requests.get(config.weatherstation_device_url, headers=headers)
            if response.status_code == 200:
                handle_partial_json(response.text)
                return {'message': "Data fetched and saved to database successfully", 'code': 200}
            else:
                return {'message': f"Failed to retrieve data with status code {response.status_code}",
                        'code': response.status_code}
    except requests.RequestException as e:
        app.logger.error(f"Error fetching data from weather station: {str(e)}")
        return {'message': str(e), 'code': 500}


def handle_partial_json(text):
    try:
        with app.app_context():
            index = text.rfind('{"result"')
            data = json.loads(text[index:])
            messages = data['result']['uplink_message']['decoded_payload']['messages']
            received_at = data['result']['received_at']
            for message in messages:
                weather_data = WeatherStationData(
                    measurement_value=message['measurementValue'],
                    measurement_type=message['type'],
                    received_at=received_at,
                    fetched_at=datetime.datetime.now()
                )
                db.session.add(weather_data)
            db.session.commit()
    except Exception as e:
        app.logger.error(f"Failed to process and save data: {str(e)}")
