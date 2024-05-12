from app import api, db
from models import WeatherStationData, WeatherForecastData
from api_models import weather_station_model, weather_forecast_model, water_usage_model, power_usage_model
from flask_restx import Resource, Namespace

from services import fetch_and_process_data, fetch_weather_forecast_range, fetch_weather_forecast

station_ns = Namespace('station', description='Endpoints for the Weather Station')
forecast_ns = Namespace('forecast', description='Endpoints for Weather Forecast')
water_ns = Namespace('water', description='Endpoints for Water usage')
power_ns = Namespace('power', description='Endpoints for Power usage')


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
        fetch_and_process_data()
        return {'status': 'fetching newest data...'}, 200


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
class WaterUsage(Resource):
    @water_ns.marshal_with(water_usage_model)
    def get(self):
        return {'water_volume': 100}, 200


@power_ns.route('/consumption')
class PowerUsage(Resource):
    @power_ns.marshal_with(power_usage_model)
    def get(self):
        return {'power_consumption': 10}, 200
