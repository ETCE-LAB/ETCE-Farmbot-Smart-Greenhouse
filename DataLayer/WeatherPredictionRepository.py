from app import db
from DataLayer.Models.models import WeatherForecastData

def add_forecast_data(forecast_data):
    db.session.add(forecast_data)

def commit_changes():
    db.session.commit()
