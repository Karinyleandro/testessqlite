from flask_restx import Namespace, Resource

api = Namespace('health', description='Health check')

@api.route('/')
class RootHealthCheck(Resource):
    def get(self):
        return {"mensagem": "Backend online! [root]"}, 200

@api.route('/health')
class HealthCheck(Resource):
    def get(self):
        return {"mensagem": "Backend online! [health]"}, 200
