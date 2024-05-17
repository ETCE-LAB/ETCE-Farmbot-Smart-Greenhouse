from flask import abort
from app import api, db
from farmbot_commands.manage_farmbot import move_to
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
        try:
            data = WeatherStationData.query.all()
            if not data:
                abort(404, 'No data found')
            return data, 200
        except Exception as e:
            station_ns.abort(500, f"Internal server error: {str(e)}")


@station_ns.route('/fetch')
class Fetch(Resource):
    def get(self):
        try:
            result = fetch_and_process_data()
            return {'status': result['message']}, result['code']
        except Exception as e:
            station_ns.abort(500, f"Internal server error: {str(e)}")


@forecast_ns.route('/get/<date>')
class Forecast(Resource):
    @forecast_ns.marshal_with(weather_forecast_model)
    def get(self, date):
        try:
            forecast_data = WeatherForecastData.query.filter_by(date=date).first()
            if forecast_data:
                return forecast_data, 200
            else:
                result = fetch_weather_forecast(date)
                if result:
                    return result, 200
                else:
                    abort(404, 'Forecast not available for this date')
        except Exception as e:
            forecast_ns.abort(500, f"Internal server error: {str(e)}")


@forecast_ns.route('/range/<start_date>/<end_date>')
class ForecastRange(Resource):
    @forecast_ns.marshal_list_with(weather_forecast_model)
    def get(self, start_date, end_date):
        try:
            forecast_data = fetch_weather_forecast_range(start_date, end_date)
            if forecast_data:
                return forecast_data, 200
            else:
                abort(404, 'No data found for the specified range')
        except Exception as e:
            forecast_ns.abort(500, f"Internal server error: {str(e)}")


@water_ns.route('/volume')
class Water(Resource):
    @water_ns.marshal_list_with(water_management_model)
    def get(self):
        try:
            data = WaterManagementData.query.all()
            if not data:
                abort(404, 'Data not found')
            return data, 200
        except Exception as e:
            water_ns.abort(500, f"Internal server error: {str(e)}")


@farmbot_ns.route('/move/<float:x>/<float:y>/<float:z>')
class Move(Resource):
    def get(self, x, y, z):
        try:
            move_to(x, y, z)
            return {
                'status': 'Reached target coordinates',
                'x': x,
                'y': y,
                'z': z
            }, 200
        except Exception as e:
            farmbot_ns.abort(500, f"Error moving FarmBot: {str(e)}")


'''
@sensor_ns.route('/data')
class SensorData(Resource):
    @sensor_ns.marshal_list_with(sensor_data_model)
    def get(self):
        data = SensorData.query.all()
        if data:
            return [{'measurement_value': item.measurement_value, 'measurement_type': item.measurement_type,
                     'received_at': item.received_at} for item in data], 200
        else:
            api.abort(404, 'Data not found')
'''
