from flask_restx import Namespace, Resource

api = Namespace('', description='Health check')  # deixa o path vazio mesmo

@api.route('/')
class RootHealth(Resource):
    def get(self):
        return {"mensagem": "Backend online!"}, 200

@api.route('/health')
class Health(Resource):
    def get(self):
        return {"mensagem": "Backend online!"}, 200
