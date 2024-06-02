from app import db


class WeatherForecastData(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String(120), nullable=False)
    max_temperature = db.Column(db.Float)
    min_temperature = db.Column(db.Float)
    sunshine_duration_minutes = db.Column(db.Integer)
    precipitation_mm = db.Column(db.Float)
    fetched_at = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<WeatherForecastData {self.date}>"

