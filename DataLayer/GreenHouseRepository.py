from app import db
from DataLayer.Models.GreenHouseModel import GreenHouseData


def get_all_temperature():
    temperatures = GreenHouseData.query.with_entities(GreenHouseData.temperature).all()
    return temperatures


def get_all_humidity():
    humidity = GreenHouseData.query.with_entities(GreenHouseData.humidity).all()
    return humidity


def get_last_temperature():
    return GreenHouseData.query.order_by(GreenHouseData.id.desc()).first()


def get_last_humidity():
    return GreenHouseData.query.order_by(GreenHouseData.id.desc()).first()


def get_temperature_by_date(date):  # TODO: fix endpoint returning empty list
    temperature_date = GreenHouseData.query.with_entities(GreenHouseData.temperature).filter_by(date=date).all()
    return [temp.temperature for temp in temperature_date]


def get_humidity_by_date(date):  # TODO: fix endpoint returning empty list
    humidity_data = GreenHouseData.query.with_entities(GreenHouseData.humidity).filter_by(date=date).all()
    return [hum.humidity for hum in humidity_data]


def add_greenhouse_data(data):
    db.session.add(data)
    db.session.commit()


def get_all_data():
    return GreenHouseData.query.all()


def get_data_by_date(date):
    data = GreenHouseData.query.with_entities(GreenHouseData.temperature, GreenHouseData.humidity).filter_by(date=date).all()
    return data
