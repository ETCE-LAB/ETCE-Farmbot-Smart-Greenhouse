from flask import abort
from flask_restx import Resource, Namespace
from Services.WeatherPredictionService import WeatherPredictionService
from app import weather_forecast_model

forecast_ns = Namespace('forecast', description='Endpoints for Weather Forecast')


@forecast_ns.route('/<date>')  # get forecast data from database
class Forecast(Resource):
    @forecast_ns.marshal_with(weather_forecast_model)
    def get(self, date):
        try:
            forecast_data, status_code = WeatherPredictionService.get_weather_forecast_by_date(date)
            if status_code == 404:
                abort(404, forecast_data['error'])
            elif status_code == 500:
                abort(500, forecast_data['error'])
            return forecast_data, 200
        except Exception as e:
            forecast_ns.abort(500, f"Internal server error: {str(e)}")


@forecast_ns.route('/<start_date>/<end_date>')  # get forecast data from database for range of dates
class ForecastRange(Resource):
    @forecast_ns.marshal_with(weather_forecast_model)
    def get(self, start_date, end_date):
        try:
            forecast_data, status_code = WeatherPredictionService.get_weather_forecast_by_date_range(start_date, end_date)
            if status_code == 404:
                abort(404, forecast_data['error'])
            elif status_code == 500:
                abort(500, forecast_data['error'])
            return forecast_data, 200
        except Exception as e:
            forecast_ns.abort(500, f"Internal server error: {str(e)}")

@forecast_ns.route('/fetch/<date>')  # get forecast from API and save to database
class FetchForecast(Resource):
    def post(self, date):
        try:
            result = WeatherPredictionService.fetch_weather_forecast(date)
            return {'status': result['message']}
        except Exception as e:
            forecast_ns.abort(500, f"Internal server error: {str(e)}")


@forecast_ns.route('/fetch/<start_date>/<end_date>')  # get forecast from API and save to database for range of dates
class FetchForecastRange(Resource):
    def post(self, start_date, end_date):
        try:
            result = WeatherPredictionService.fetch_weather_forecast_range(start_date, end_date)
            if result['code'] == 500:
                abort(500, result['message'])
            return {'status': result['message']}, result['code']
        except Exception as e:
            forecast_ns.abort(500, f"Internal server error: {str(e)}")


@forecast_ns.route('/<start_date>/<end_date>')
class ForecastRange(Resource):
    @forecast_ns.marshal_with(weather_forecast_model)
    def get(self, start_date, end_date):
        try:
            forecast_data, status_code = WeatherPredictionService.get_weather_forecast_range(start_date, end_date)
            if status_code == 404:
                abort(404, forecast_data['error'])
            elif status_code == 500:
                abort(500, forecast_data['error'])
            return forecast_data, 200
        except Exception as e:
            forecast_ns.abort(500, f"Internal server error: {str(e)}")
