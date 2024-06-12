from flask_restx import Resource, Namespace
from Services.FarmBotServices.MeasureSoilMoisture import measure_soil_moisture_sequence
from Services.FarmBotServices.MoveFarmBot import move_to
from Services.FarmBotServices.WaterField import execute_watering_sequence

farmbot_ns = Namespace('farmbot', description='Endpoints for FarmBot')


@farmbot_ns.route('/moveTo/<float:x>/<float:y>/<float:z>')
class Move(Resource):
    def get(self, x, y, z):
        try:
            move_to(x, y, z)
            return {
                'status': 'Reached target coordinates',
                'x': x,
                'y': y,
                'z': z
            }, 200
        except Exception as e:
            farmbot_ns.abort(500, f"Error moving FarmBot: {str(e)}")


@farmbot_ns.route('/waterField')
class WaterField(Resource):
    def get(self):
        try:
            execute_watering_sequence()
            return {
                'status': 'Watering sequence completed'
            }, 200
        except Exception as e:
            farmbot_ns.abort(500, f"Error executing watering sequence: {str(e)}")


@farmbot_ns.route('/measure/measureSoilMoisture')
class MeasureSoil(Resource):
    def get(self):
        try:
            measure_soil_moisture_sequence()
            return {
                'status': 'Soil moisture measurement completed'
            }, 200
        except Exception as e:
            farmbot_ns.abort(500, f"Error measuring soil moisture: {str(e)}")
