from flask_restx import Resource, Namespace
from Services import GreenHouseService
from app import greenhouse_model

greenhouse_ns = Namespace('greenhouse', description='Endpoints for Greenhouse management')

"""
@greenhouse_ns.route('/temperature')
class Temperature(Resource):
    @greenhouse_ns.marshal_list_with(greenhouse_model)
    def get(self):
        try:
            data = GreenHouseService.get_all_temperature()
            if not data:
                return [], 200
            else:
                return data, 200
        except Exception as e:
            greenhouse_ns.abort(500, f"Internal server error: {str(e)}")


@greenhouse_ns.route('/humidity')
class Humidity(Resource):
    @greenhouse_ns.marshal_list_with(greenhouse_model)
    def get(self):
        try:
            data = GreenHouseService.get_all_humidity()
            if not data:
                return [], 200
            else:
                return data, 200
        except Exception as e:
            greenhouse_ns.abort(500, f"Internal server error: {str(e)}")
"""


@greenhouse_ns.route('/temperature/<date>')
class Temperature(Resource):
    @greenhouse_ns.marshal_list_with(greenhouse_model)
    def get(self, date):
        try:
            data = GreenHouseService.get_temperature_by_date(date)
            if not data:
                return [], 200
            else:
                return data, 200
        except Exception as e:
            greenhouse_ns.abort(500, f"Internal server error: {str(e)}")


@greenhouse_ns.route('temperature/<start_date>/<end_date>')
class HumidityRange(Resource):
    @greenhouse_ns.marshal_list_with(greenhouse_model)
    def get(self, start_date, end_date):
        try:
            data = GreenHouseService.get_temperature_range(start_date, end_date)
            return data, 200
        except Exception as e:
            greenhouse_ns.abort(500, f"Internal server error: {str(e)}")


@greenhouse_ns.route('/humidity/<date>')
class Humidity(Resource):
    @greenhouse_ns.marshal_list_with(greenhouse_model)
    def get(self, date):
        try:
            data = GreenHouseService.get_humidity_by_date(date)
            if not data:
                return [], 200
            else:
                return data, 200
        except Exception as e:
            greenhouse_ns.abort(500, f"Internal server error: {str(e)}")


@greenhouse_ns.route('humidity/<start_date>/<end_date>')
class HumidityRange(Resource):
    @greenhouse_ns.marshal_list_with(greenhouse_model)
    def get(self, start_date, end_date):
        try:
            data = GreenHouseService.get_humidity_range(start_date, end_date)
            return data, 200
        except Exception as e:
            greenhouse_ns.abort(500, f"Internal server error: {str(e)}")


@greenhouse_ns.route('/measure')
class All(Resource):
    def post(self):
        try:
            data = GreenHouseService.measure_and_store_data()
            return data, 200
        except Exception as e:
            greenhouse_ns.abort(500, f"Internal server error: {str(e)}")


@greenhouse_ns.route('/all')
class All(Resource):
    @greenhouse_ns.marshal_list_with(greenhouse_model)
    def get(self):
        try:
            data = GreenHouseService.get_all_data()
            return data, 200
        except Exception as e:
            greenhouse_ns.abort(500, f"Internal server error: {str(e)}")


@greenhouse_ns.route('/data/<date>')
class DateData(Resource):
    @greenhouse_ns.marshal_list_with(greenhouse_model)
    def get(self, date):
        try:
            data = GreenHouseService.get_data_by_date(date)
            return data, 200
        except Exception as e:
            greenhouse_ns.abort(500, f"Error: {str(e)}")
