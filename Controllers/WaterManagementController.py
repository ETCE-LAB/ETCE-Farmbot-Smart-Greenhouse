from flask import abort
from flask_restx import Resource, Namespace

from DataLayer import WaterManagementRepository
from DataLayer.WaterManagementRepository import get_all_water_data, get_volume_by_date
from Services.WaterManagementService import WaterManagementService
from app import water_management_model

water_ns = Namespace('water', description='Endpoints for Water management')


@water_ns.route('/volume/all')
class Water(Resource):
    @water_ns.marshal_list_with(water_management_model)
    def get(self):
        try:
            data = get_all_water_data()  # TODO: replace with service layer and if list empty return empty list
            if not data:
                abort(404, 'Data not found')
            return data, 200
        except Exception as e:
            water_ns.abort(500, f"Internal server error: {str(e)}")


@water_ns.route('/volume/last')
class Water(Resource):
    @water_ns.marshal_with(water_management_model)
    def get(self):
        try:
            data = get_all_water_data()  # TODO: replace with service  layer
            if not data:
                abort(404, 'Data not found in database')
            return data[-1], 200
        except Exception as e:
            water_ns.abort(500, f"Internal server error: {str(e)}")


@water_ns.route('/volume/<string:date>')
class Water(Resource):
    @water_ns.marshal_list_with(water_management_model)
    def get(self, date):
        try:
            data = WaterManagementRepository.get_volume_by_date(date)
            if not data:
                abort(404, 'Data not found')
            return data, 200
        except Exception as e:
            water_ns.abort(500, f"Internal server error: {str(e)}")


@water_ns.route('/measure')
class Water(Resource):
    def post(self):
        try:
            WaterManagementService.measure_and_store_volume()
            return {'status': 'Water measurement successful'}, 200
        except Exception as e:
            return {'status': f"Internal server error: {str(e)}"}, 500
