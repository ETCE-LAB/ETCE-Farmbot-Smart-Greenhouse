from flask import abort
from flask_restx import Resource, Namespace

from DataLayer.Models.WaterManagementModel import WaterManagementData
from app import water_management_model

water_ns = Namespace('water', description='Endpoints for Water management')


@water_ns.route('/volume')
class Water(Resource):
    @water_ns.marshal_list_with(water_management_model)
    def get(self):
        try:
            data = WaterManagementData.query.all()
            if not data:
                abort(404, 'Data not found')
            return data, 200
        except Exception as e:
            water_ns.abort(500, f"Internal server error: {str(e)}")
