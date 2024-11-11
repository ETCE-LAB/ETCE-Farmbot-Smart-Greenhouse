from datetime import datetime
from app import db


class GreenHouseData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(120), nullable=False)
    sensor = db.Column(db.String(120), nullable=False)
    cordinates = db.Column(db.String(120), nullable=False)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    soilmoisture = db.Column(db.Float)
    fetched_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<GreenHouseData  {self.date} {self.sensor} {self.cordinates} {self.temperature} {self.humidity} {self.soilmoisture}>"
