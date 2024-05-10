import requests
import config
from app import db
from models import WeatherStationData, WeatherForecastData
import json
import datetime


def fetch_weather_forecast(date):
    response = requests.get(config.weather_forecast_url.format(date=date))
    response.raise_for_status()
    data = response.json()
    forecast_data = None
    for forecast in data['forecasts']:
        if forecast['date'] == date:
            forecast_data = WeatherForecastData(
                date=date,
                max_temperature=forecast['temperature']['max'],
                min_temperature=forecast['temperature']['min'],
                sunshine_duration_minutes=int(forecast['sunshine_duration'] / 60),
                precipitation_mm=forecast['precipitation']
            )
            db.session.add(forecast_data)
            db.session.commit()
            return {
                'date': date,
                'max_temperature': forecast['temperature']['max'],
                'min_temperature': forecast['temperature']['min'],
                'sunshine_duration_minutes': int(forecast['sunshine_duration'] / 60),
                'precipitation_mm': forecast['precipitation']
            }
    if not forecast_data:
        raise ValueError('Forecast not found for the given date')


def fetch_weather_forecast_range(start_date, end_date):
    response = requests.get(config.weather_forecast_range_url.format(start_date=start_date, end_date=end_date))
    response.raise_for_status()
    data = response.json()
    forecast_list = []
    for forecast in data['forecasts']:
        forecast_data = WeatherForecastData(
            date=forecast['date'],
            max_temperature=forecast['temperature']['max'],
            min_temperature=forecast['temperature']['min'],
            sunshine_duration_minutes=int(forecast['sunshine_duration'] / 60),
            precipitation_mm=forecast['precipitation']
        )
        db.session.add(forecast_data)
        forecast_list.append({
            'date': forecast['date'],
            'max_temperature': forecast['temperature']['max'],
            'min_temperature': forecast['temperature']['min'],
            'sunshine_duration_minutes': int(forecast['sunshine_duration'] / 60),
            'precipitation_mm': forecast['precipitation']
        })
    db.session.commit()
    return forecast_list


def fetch_and_process_data():
    response = requests.get(config.weatherstation_device_url)
    if response.status_code == 200:
        data = json.loads(response.text)
        for record in data['records']:
            weather_data = WeatherStationData(
                measurement_value=record['value'],
                measurement_type=record['type'],
                received_at=record['timestamp']
            )
            db.session.add(weather_data)
        db.session.commit()
    else:
        print(f"Failed to retrieve data with status code {response.status_code}")


def handle_partial_json(text):
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
