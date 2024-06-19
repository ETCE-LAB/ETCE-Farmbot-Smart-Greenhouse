from flask import abort
from flask_restx import Resource, Namespace
from Services.WaterManagementService import WaterManagementService
from app import water_management_model

water_ns = Namespace('water', description='Endpoints for Water management')


@water_ns.route('/volume/all')
class Water(Resource):
    @water_ns.marshal_list_with(water_management_model)
    def get(self):
        try:
            data = WaterManagementService.get_all_water_data()
            if not data:
                return [], 200
            return data, 200
        except Exception as e:
            water_ns.abort(500, f"Internal server error: {str(e)}")


@water_ns.route('/volume/last')
class Water(Resource):
    @water_ns.marshal_with(water_management_model)
    def get(self):
        try:
            data = WaterManagementService.get_last_water_data()
            if not data:
                abort(404, 'Data not found')
            return data, 200
        except Exception as e:
            water_ns.abort(500, f"Internal server error: {str(e)}")


@water_ns.route('/volume/<string:date>')
class Water(Resource):
    @water_ns.marshal_list_with(water_management_model)
    def get(self, date):
        try:
            data = WaterManagementService.get_volume_by_date(date)
            if not data:
                abort(404, 'Data not found')
            return data, 200
        except Exception as e:
            water_ns.abort(500, f"Internal server error: {str(e)}")


@water_ns.route('/volume/<start_date>/<end_date>')
class Water(Resource):
    @water_ns.marshal_list_with(water_management_model)
    def get(self, start_date, end_date):
        try:
            data = WaterManagementService.get_volume_by_date_range(start_date, end_date)
            if not data:
                abort(404, 'Data not found')
            return data, 200
        except Exception as e:
            water_ns.abort(500, f"Internal server error: {str(e)}")


@water_ns.route('/measure')
class Water(Resource):
    def post(self):
        try:
            WaterManagementService.measure_and_store_volume(self)
            return {'status': 'Water measurement successful'}, 200
        except Exception as e:
            return {'status': f"Internal server error: {str(e)}"}, 500
