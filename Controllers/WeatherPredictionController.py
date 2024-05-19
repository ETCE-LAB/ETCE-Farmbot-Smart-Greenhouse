from flask import abort
from werkzeug.exceptions import NotFound

from app import api, db
from farmbot_commands.manage_farmbot import move_to
from DataLayer.Models.models import WeatherStationData, WeatherForecastData, WaterManagementData
from DataLayer.Models.api_models import weather_station_model, weather_forecast_model, water_management_model  # , sensor_data_model
from flask_restx import Resource, Namespace
from Services.services import fetch_and_process_data, fetch_weather_forecast_range, fetch_weather_forecast
from datetime import datetime

forecast_ns = Namespace('forecast', description='Endpoints for Weather Forecast')


@forecast_ns.route('/get/<date>')
class Forecast(Resource):
    @forecast_ns.marshal_with(weather_forecast_model)
    def get(self, date):
        try:
            try:
                valid_date = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                abort(400, "Invalid date format. Please use YYYY-MM-DD format.")

            forecast_data = WeatherForecastData.query.filter_by(date=valid_date).first()
            if forecast_data:
                return forecast_data, 200
            else:
                abort(404, 'Forecast not available for this date')
        except NotFound as e:
            forecast_ns.abort(404, str(e))
        except Exception as e:
            forecast_ns.abort(500, f"Internal server error: {str(e)}")

