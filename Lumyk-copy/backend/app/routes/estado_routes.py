from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required
from backend.app.controllers import EstadoController

api = Namespace('estados', description='Operações relacionadas a Estados')

estado_model = api.model('Estado', {
    'nome': fields.String(required=True),
    'taxa_frete': fields.Float(required=True)  
})

estado_get = api.model('EstadoResponse', {
    'id': fields.String(required=True),
    'nome': fields.String(required=True),
    'taxa_frete': fields.Float(required=True)  
    
})

@api.route('/')
class EstadoListar(Resource):
    @api.marshal_list_with(estado_get)
    def get(self):
        return EstadoController.listar_estados()[0]

    @api.expect(estado_model)
    @api.doc(security='Bearer Auth')
    @jwt_required()
    @api.response(201, 'Estado criado com sucesso!')
    @api.response(400, 'Erro de validação')
    def post(self):
        data = request.get_json()
        return EstadoController.criar_estado(data)

@api.route('/<string:id>')
@api.param('id', 'ID do estado')
class EstadoManipular(Resource):
    @api.marshal_with(estado_get)
    def get(self, id):
        return EstadoController.buscar_estado_por_id(id)[0]

    @api.expect(estado_model)
    @api.doc(security='Bearer Auth')
    @api.response(200, 'Estado atualizado com sucesso!')
    @api.response(400, 'Erro de validação')
    def put(self, id):
        data = request.get_json()
        return EstadoController.atualizar_estado(id, data)

    @api.doc(security='Bearer Auth')
    @api.response(200, 'Estado deletado com sucesso!')
    def delete(self, id):
        return EstadoController.deletar_estado(id)