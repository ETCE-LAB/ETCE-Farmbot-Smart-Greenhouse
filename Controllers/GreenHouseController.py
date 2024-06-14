from flask_restx import Resource, Namespace
from Services import GreenHouseService
from app import greenhouse_model

greenhouse_ns = Namespace('greenhouse', description='Endpoints for Greenhouse management')


@greenhouse_ns.route('/temperature')
class Temperature(Resource):
    @greenhouse_ns.marshal_list_with(greenhouse_model)
    def get(self):
        try:
            data = GreenHouseService.get_all_temperature()
            if not data:
                return [], 200
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
            return data, 200
        except Exception as e:
            greenhouse_ns.abort(500, f"Internal server error: {str(e)}")


@greenhouse_ns.route('/temperature/<date>')
class Temperature(Resource):
    @greenhouse_ns.marshal_list_with(greenhouse_model)
    def get(self, date):
        try:
            data = GreenHouseService.get_temperature_by_date(date)
            if not data:
                return [], 200
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
            return data, 200
        except Exception as e:
            greenhouse_ns.abort(500, f"Internal server error: {str(e)}")
#  TODO: add range endpoint

@greenhouse_ns.route('/measure')
class All(Resource):
    def post(self):
        try:
            data = GreenHouseService.measure_and_store_data()
            if not data:
                return [], 200
            return data, 200
        except Exception as e:
            greenhouse_ns.abort(500, f"Internal server error: {str(e)}")