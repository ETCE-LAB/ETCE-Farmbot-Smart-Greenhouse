from datetime import datetime
from app import db


class WaterManagementData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(120), nullable=False)
    volume = db.Column(db.Float)
    fetched_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<WaterManagementData {self.volume} {self.date}>"