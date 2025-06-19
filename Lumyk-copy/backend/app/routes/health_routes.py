from flask_restx import Namespace, Resource

health = Namespace('', description='Health check (root)')

@health.route('/')
class HealthCheck(Resource):
    def get(self):
        return {'mensagem': 'Backend online!'}, 200
