from datetime import datetime
from app import db
from DataLayer.Models.WaterManagementModel import WaterManagementData


def get_all_water_data():
    return WaterManagementData.query.all()


def add_water_data(volume):
    new_data = WaterManagementData(
        date=datetime.now().strftime("%Y-%m-%d %H:%M"),
        volume=int(round(volume / 1000)),
        fetched_at=datetime.utcnow()
    )
    db.session.add(new_data)
    db.session.commit()
