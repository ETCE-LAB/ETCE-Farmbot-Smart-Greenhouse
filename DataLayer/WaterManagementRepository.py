from app import db
from DataLayer.Models.WaterManagementModel import WaterManagementData


def get_all_water_data():
    return WaterManagementData.query.all()


def get_last_water_data():
    return WaterManagementData.query.order_by(WaterManagementData.id.desc()).first()


def get_volume_by_date(date):
    return WaterManagementData.query.filter_by(date=date).all()


def get_volume_by_date_range(start_date, end_date):
    return WaterManagementData.query.filter(WaterManagementData.date.between(start_date, end_date)).all()


def delete_water_data_by_id(id):
    data = WaterManagementData.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()


def add_water_data(data):
    db.session.add(data)
    db.session.commit()
