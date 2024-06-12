from app import db
from DataLayer.Models.GreenHouseModel import GreenHouseData


def get_all_temperature():
    return GreenHouseData.query.filter(GreenHouseData.temperature).all()


def get_all_humidity():
    return GreenHouseData.query.filter(GreenHouseData.humidity).all()


def get_last_temperature():
    return GreenHouseData.query.order_by(GreenHouseData.id.desc()).first()


def get_last_humidity():
    return GreenHouseData.query.order_by(GreenHouseData.id.desc()).first()


def get_temperature_by_date(date):
    return GreenHouseData.query.filter_by(date=date).all()


def get_humidity_by_date(date):
    return GreenHouseData.query.filter_by(date=date).all()


def add_greenhouse_data(data):
    db.session.add(data)
    db.session.commit()
