from flask_restx import fields


def create_models(api):
    weather_station_model = api.model('WeatherStationData', {
        'id': fields.Integer(description='The unique identifier of the measurement'),
        'measurement_value': fields.Float(required=True, description='Value of the measurement'),
        'measurement_type': fields.String(required=True, description='Type of the measurement'),
        'received_at': fields.String(required=True, description='ISO date string when the measurement was received')
    })

    weather_forecast_model = api.model('WeatherForecastData', {
        'id': fields.Integer(description='The unique identifier of the forecast'),
        'date': fields.String(required=True, description='The date of the forecast'),
        'max_temperature': fields.Float(description='The maximum temperature of the day'),
        'min_temperature': fields.Float(description='The minimum temperature of the day'),
        'sunshine_duration_minutes': fields.Integer(description='The duration of sunshine in minutes'),
        'precipitation_mm': fields.Float(description='The amount of precipitation over the day in mm. 1mm = 1l/m²')
    })

    water_management_model = api.model('WaterManagementData', {
        'id': fields.Integer(description='The unique identifier of the measurement'),
        'date': fields.String(required=True, description='The date of the reading'),
        'volume': fields.Float(description='The stored volume of water in liters')
    })

    return weather_station_model, weather_forecast_model, water_management_model
