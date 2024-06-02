from app import db


class WeatherStationData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    measurement_value = db.Column(db.Float, nullable=False)
    measurement_type = db.Column(db.String(50), nullable=False)
    received_at = db.Column(db.String(120), nullable=False)
    fetched_at = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<WeatherStationData {self.measurement_type} {self.received_at}>"