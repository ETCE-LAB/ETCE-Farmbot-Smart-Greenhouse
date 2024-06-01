from flask import abort
from flask_restx import Resource, Namespace
from DataLayer import WeatherStationRepository
from DataLayer.Models.WeatherStationModel import WeatherStationData
from Services.WeatherStationService import fetch_weather_station_data
from app import weather_station_model

station_ns = Namespace('station', description='Endpoints for the Weather Station')


@station_ns.route('/data')
class Data(Resource):
    @station_ns.marshal_list_with(weather_station_model)
    def get(self):
        try:
            data = WeatherStationRepository.get_all_weather_data()
            if not data:
                abort(404, 'No data found')
            return data, 200
        except Exception as e:
            station_ns.abort(500, f"Internal server error: {str(e)}")


@station_ns.route('/fetch')
class Fetch(Resource):
    def get(self):
        try:
            result = fetch_weather_station_data()
            return {'status': result['message']}, result['code']
        except Exception as e:
            station_ns.abort(500, f"Internal server error: {str(e)}")
