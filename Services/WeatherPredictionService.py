# import json
from datetime import datetime

import requests
from flask import jsonify

import config
from DataLayer.Models.WeatherForecastModel import WeatherForecastData
from DataLayer.WeatherPredictionRepository import add_forecast_data, commit_changes
from app import app


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
                    # db.session.add(forecast_data)
                    add_forecast_data(forecast_data)
            # db.session.commit()
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
                    add_forecast_data(forecast_data)

            commit_changes()
            print(datetime.now().strftime('%d-%m %H:%M') + " Range forecast fetch successful, data saved.")

        else:
            print("Date range not found in the data.")


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
