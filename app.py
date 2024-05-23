from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smart_greenhouse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app, version='3.0', title='FarmBot API',
          description='Endpoints for FarmBot, SmartGreenhouse, and Weather Station')

from Controllers.WeatherStationController import station_ns,water_ns,farmbot_ns
from Controllers.WeatherPredictionController import  forecast_ns

print("Registering namespaces...")
api.add_namespace(station_ns)
api.add_namespace(forecast_ns)
api.add_namespace(water_ns)
api.add_namespace(farmbot_ns)
print("Namespaces registered.")

'''
api.add_namespace(sequence_ns)
api.add_namespace(sensor_ns)
'''

if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(debug=True)
