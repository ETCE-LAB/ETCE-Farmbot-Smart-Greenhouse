from app import db


def add_weather_data(weather_data):
    db.session.add(weather_data)


def commit_changes():
    db.session.commit()
