from datetime import datetime
import requests
import config
from DataLayer import WeatherPredictionRepository
from DataLayer.Models.WeatherPredictionModel import WeatherForecastData
from DataLayer.WeatherPredictionRepository import (
    add_forecast_data,
    commit_changes,
    update_forecast_data,
)
from app import app
from Services.Interfaces.IWeatherPredictionService import IWeatherPredictionService


class WeatherPredictionService(IWeatherPredictionService):
    @staticmethod
    def fetch_weather_forecast(date):
        try:
            response = requests.get(config.weather_forecast_url)
            response.raise_for_status()
            data = response.json()
            forecasts = []
            for i, day in enumerate(data['daily']['time']):
                if day == date:
                    sunshine_duration_minutes = int(data['daily']['sunshine_duration'][i] / 60)
                    forecast_data = WeatherForecastData(
                        date=day,
                        max_temperature=data['daily']['temperature_2m_max'][i],
                        min_temperature=data['daily']['temperature_2m_min'][i],
                        sunshine_duration_minutes=sunshine_duration_minutes,
                        precipitation_mm=data['daily']['precipitation_sum'][i],
                        fetched_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    )
                    forecasts.append(forecast_data)
            WeatherPredictionRepository.add_forecasts(forecasts)
            return {"message": "Forecast fetch successful, data saved.", "code": response.status_code}

        except requests.HTTPError as e:
            print("HTTP Error:", e)
            return {"message": f"HTTP error occurred: {e}", "code": response.status_code}
        except requests.RequestException as e:
            print("Request Exception:", e)
            return {"message": f"Request exception occurred: {e}", "code": response.status_code}
        except Exception as e:
            print("General Exception:", e)
            return {"message": f"An error occurred: {e}", "code": 500}

    @staticmethod
    def fetch_weather_forecast_range(start_date, end_date):
        with app.app_context():
            try:
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

                        forecast_data = WeatherPredictionRepository.get_forecast_data_by_date(date)
                        if forecast_data:
                            update_forecast_data(
                                forecast_data, max_temperature, min_temperature, sunshine_duration_minutes,
                                precipitation_mm
                            )
                        else:
                            forecast_data = WeatherForecastData(
                                date=date,
                                max_temperature=max_temperature,
                                min_temperature=min_temperature,
                                sunshine_duration_minutes=sunshine_duration_minutes,
                                precipitation_mm=precipitation_mm,
                                fetched_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            )
                            add_forecast_data(forecast_data)

                    commit_changes()
                    print(datetime.now().strftime('%d-%m %H:%M') + " Range forecast fetch successful, data saved.")
                    return {"message": "Range forecast fetch successful, data saved.", "code": response.status_code}

                else:
                    print("Date range not found in the data.")
                    return {"message": "Date range not found in the data.", "code": 404}

            except requests.HTTPError as e:
                print("HTTP Error:", e)
                return {"message": f"HTTP error occurred: {e}", "code": response.status_code}
            except requests.RequestException as e:
                print("Request Exception:", e)
                return {"message": f"Request exception occurred: {e}", "code": response.status_code}
            except Exception as e:
                print("General Exception:", e)
                return {"message": f"An error occurred: {e}", "code": 500}

    @staticmethod
    def get_weather_forecast_by_date(date):
        try:
            forecast_data = WeatherPredictionRepository.get_forecast_data_by_date(date)
            if forecast_data:
                return {
                    'date': forecast_data.date,
                    'max_temperature': forecast_data.max_temperature,
                    'min_temperature': forecast_data.min_temperature,
                    'sunshine_duration_minutes': forecast_data.sunshine_duration_minutes,
                    'precipitation_mm': forecast_data.precipitation_mm
                }, 200
            else:
                return {'error': 'No forecast data available for this date'}, 404
        except Exception as e:
            return {'error': f"An error occurred: {e}"}, 500

    @classmethod
    def get_weather_forecast_by_date_range(cls, start_date, end_date):
        try:
            forecast_data = WeatherPredictionRepository.get_forecast_data_by_date_range(start_date, end_date)
            if forecast_data:
                return forecast_data, 200
            else:
                return {'error': 'No forecast data available for this date range'}, 404
        except Exception as e:
            return {'error': f"An error occurred: {e}"}, 500
