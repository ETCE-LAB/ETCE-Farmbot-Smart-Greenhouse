from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smart_greenhouse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app, version='2.0', title='FarmBot API',
          description='Endpoints for FarmBot, SmartGreenhouse, and Weather Station')

from resources import station_ns, forecast_ns, water_ns, sequence_ns, sensor_ns

api.add_namespace(station_ns)
api.add_namespace(forecast_ns)
api.add_namespace(water_ns)
api.add_namespace(sequence_ns)
api.add_namespace(sensor_ns)

