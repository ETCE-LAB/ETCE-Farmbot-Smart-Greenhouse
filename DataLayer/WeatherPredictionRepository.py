from app import db
from DataLayer.Models.WeatherPredictionModel import WeatherForecastData


def add_forecast_data(forecast_data):
    db.session.add(forecast_data)


def commit_changes():
    db.session.commit()


def get_forecast_data_by_date(date):
    return WeatherForecastData.query.filter_by(date=date).first()


def update_forecast_data(forecast_data, max_temperature, min_temperature, sunshine_duration_minutes, precipitation_mm):
    forecast_data.max_temperature = max_temperature
    forecast_data.min_temperature = min_temperature
    forecast_data.sunshine_duration_minutes = sunshine_duration_minutes
    forecast_data.precipitation_mm = precipitation_mm
    add_forecast_data(forecast_data)
