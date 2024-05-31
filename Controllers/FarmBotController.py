from flask_restx import Resource, Namespace
from Services.FarmBotServices.MoveFarmBot import move_to

farmbot_ns = Namespace('farmbot', description='Endpoints for FarmBot')


@farmbot_ns.route('/move/<float:x>/<float:y>/<float:z>')
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
