from flask import abort
from flask_restx import Resource, Namespace
from DataLayer import WeatherStationRepository
from Services.WeatherStationService import WeatherStationService
from app import weather_station_model

station_ns = Namespace('station', description='Endpoints for the Weather Station')

weather_station_service = WeatherStationService()


@station_ns.route('/all')
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


@station_ns.route('/<string:date>')
class DataByDate(Resource):
    @station_ns.marshal_list_with(weather_station_model)
    def get(self, date):
        data, error = weather_station_service.fetch_weather_data_by_date(date)
        if error:
            if 'No data found' in error:
                abort(404, error)
            elif 'Invalid date format' in error:
                abort(400, error)
            else:
                abort(500, error)
        return data, 200


@station_ns.route('/<string:start_date>/<string:end_date>')
class DataRange(Resource):
    @station_ns.marshal_list_with(weather_station_model)
    def get(self, start_date, end_date):
        data, error = weather_station_service.fetch_weather_data_by_date_range(start_date, end_date)
        if error:
            if 'No data found' in error:
                abort(404, error)
            elif 'Invalid date format' in error:
                abort(400, error)
            else:
                abort(500, error)
        return data, 200

@station_ns.route('/fetch')
class Fetch(Resource):
    def post(self):
        try:
            result = weather_station_service.fetch_weather_station_data()
            return {'status': result['message']}, result['code']
        except Exception as e:
            station_ns.abort(500, f"Internal server error: {str(e)}")
