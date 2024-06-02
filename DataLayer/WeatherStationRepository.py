from DataLayer.Models.WeatherStationModel import WeatherStationData
from app import db
from sqlalchemy import func

def add_weather_data(weather_data):
    db.session.add(weather_data)
    db.session.commit()


def get_weather_data_by_date(date):
    return WeatherStationData.query.filter(
        func.date(WeatherStationData.fetched_at) == date.date()
    ).all()


def get_all_weather_data():
    return WeatherStationData.query.all()
