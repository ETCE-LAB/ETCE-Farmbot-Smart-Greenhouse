from app import api, db
from farmbot_commands.move_farmbot import move_to
from models import WeatherStationData, WeatherForecastData, WaterManagementData
from api_models import weather_station_model, weather_forecast_model, water_management_model  # , sensor_data_model
from flask_restx import Resource, Namespace
from services import fetch_and_process_data, fetch_weather_forecast_range, fetch_weather_forecast

station_ns = Namespace('station', description='Endpoints for the Weather Station')
forecast_ns = Namespace('forecast', description='Endpoints for Weather Forecast')
water_ns = Namespace('water', description='Endpoints for Water management')
sensor_ns = Namespace('sensor', description='Endpoints for Sensor data')
sequence_ns = Namespace('sequence', description='Endpoints for managing sequences')
farmbot_ns = Namespace('farmbot', description='Endpoints for FarmBot')


@station_ns.route('/data')
class Data(Resource):
    @station_ns.marshal_list_with(weather_station_model)
    def get(self):
        data = WeatherStationData.query.all()
        if data:
            return [{'measurement_value': item.measurement_value, 'measurement_type': item.measurement_type,
                     'received_at': item.received_at} for item in data], 200
        else:
            api.abort(404, 'Data not found')


@station_ns.route('/fetch')
class Fetch(Resource):
    @staticmethod
    def get():
        result = fetch_and_process_data()
        return {'status': result['message']}, result['code']


@forecast_ns.route('/get/<date>')
class Forecast(Resource):
    @forecast_ns.marshal_list_with(weather_forecast_model)
    def get(self, date):
        forecast_data = WeatherForecastData.query.filter_by(date=date).first()
        if forecast_data:
            return {col.name: getattr(forecast_data, col.name) for col in forecast_data.__table__.columns}, 200
        else:
            forecast_data = fetch_weather_forecast(date)
            return forecast_data, 200


@forecast_ns.route('/range/<start_date>/<end_date>')
class ForecastRange(Resource):
    @forecast_ns.marshal_list_with(weather_forecast_model)
    def get(self, start_date, end_date):
        forecast_data = fetch_weather_forecast_range(start_date, end_date)
        if forecast_data:
            return forecast_data, 200
        else:
            api.abort(404, 'No data found for the specified range')


@water_ns.route('/volume')
class Water(Resource):
    @water_ns.marshal_list_with(water_management_model)
    def get(self):
        data = WaterManagementData.query.all()
        if data:
            return [{'date': item.date, 'volume': item.volume} for item in data], 200
        else:
            api.abort(404, 'Data not found')


@water_ns.route('/measure')
# Placeholder for measuring water volume
class Fetch(Resource):
    @staticmethod
    def get():
        return {'status': 'Not implemented yet'}, 501


@farmbot_ns.route('/move/<float:x>/<float:y>/<float:z>')
class Move(Resource):
    @staticmethod
    def get(x, y, z):
        move_to(x, y, z)
        return {
            'status': 'Moving FarmBot',
            'x': x,
            'y': y,
            'z': z
        }, 200


'''@sensor_ns.route('/data')
class SensorData(Resource):
    @sensor_ns.marshal_list_with(sensor_data_model)
    def get(self):
        data = SensorData.query.all()
        if data:
            return [{'measurement_value': item.measurement_value, 'measurement_type': item.measurement_type,
                     'received_at': item.received_at} for item in data], 200
        else:
            api.abort(404, 'Data not found')


@sequence_ns.route('/sequence<sequence_id>')  # send sequenz_id to FarmBot
# Placeholder for starting a sequence
class Fetch(Resource):
    @staticmethod
    def get(sequence_id):
        return {'status': 'Not implemented yet',
                'sequence_id': sequence_id,
                'sequenz_name': 'Placeholder'
                }, 501
'''
