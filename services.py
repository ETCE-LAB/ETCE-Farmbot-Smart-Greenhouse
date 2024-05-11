import requests
import config
from app import db
from models import WeatherStationData, WeatherForecastData
import json
import datetime


def fetch_weather_forecast(date):
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


def fetch_weather_forecast_range(start_date, end_date):
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
