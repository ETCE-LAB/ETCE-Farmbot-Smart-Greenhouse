from app import db


class WeatherStationData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    measurement_value = db.Column(db.Float, nullable=False)
    measurement_type = db.Column(db.String(50), nullable=False)
    received_at = db.Column(db.String(120), nullable=False)
    fetched_at = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<WeatherStationData {self.measurement_type} {self.received_at}>"


class WeatherForecastData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(120), nullable=False)
    max_temperature = db.Column(db.Float)
    min_temperature = db.Column(db.Float)
    sunshine_duration_minutes = db.Column(db.Integer)
    precipitation_mm = db.Column(db.Float)
    fetched_at = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<WeatherForecastData {self.date}>"


class WaterManagementData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(120), nullable=False)
    volume = db.Column(db.Float)

    def __repr__(self):
        return f"<WaterManagementData {self.water_usage} {self.received_at}>"


'''class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    measurement_value = db.Column(db.Float, nullable=False)
    measurement_type = db.Column(db.String(50), nullable=False)
    received_at = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<SensorData {self.measurement_type} {self.received_at}>"
'''