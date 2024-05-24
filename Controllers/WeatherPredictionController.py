from datetime import datetime

from flask import abort
from flask_restx import Resource, Namespace
from werkzeug.exceptions import NotFound

from DataLayer.Models.api_models import weather_forecast_model  # , sensor_data_model
from DataLayer.Models.models import WeatherForecastData

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

