from DataLayer.Models.WeatherStationModel import WeatherStationData
from app import db


def add_weather_data(weather_data):
    db.session.add(weather_data)
    db.session.commit()


def get_all_weather_data():
    return WeatherStationData.query.all()
