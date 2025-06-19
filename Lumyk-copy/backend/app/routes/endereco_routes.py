from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required
from backend.app.controllers import EnderecoController
from backend.app.middlewares.autorizacao_endereco import autorizacao_endereco

api = Namespace('enderecos', description='Operações relacionadas a Endereços')

endereco_model = api.model('Endereco', {
    'id_estado': fields.String(required=True, description='ID do Estado'),
    'numero': fields.Integer(required=True, description='Número'),
    'bairro': fields.String(required=True, description='Bairro'),
    'rua': fields.String(required=True, description='Rua'),
})

endereco_response = api.model('EnderecoResponse', {
    'id': fields.String(description='ID do Endereço'),
    'id_usuario': fields.String(description='ID do Usuário'),
    'id_estado': fields.String(description='ID do Estado'),
    'numero': fields.Integer(description='Número'),
    'bairro': fields.String(description='Bairro'),
    'rua': fields.String(description='Rua'),
})


@api.route('/')
class EnderecoList(Resource):
    @api.marshal_list_with(endereco_response)
    def get(self):
        return EnderecoController.listar_enderecos()[0]

    @api.expect(endereco_model, validate=False)
    @api.doc(security='Bearer Auth')
    @jwt_required()
    @api.response(201, 'Endereço criado com sucesso!')
    def post(self):
        data = request.get_json()
        return EnderecoController.criar_endereco(data)


@api.route('/<string:id>')
@api.param('id', 'ID do Endereço')
class EnderecoResource(Resource):
    @api.marshal_with(endereco_response)
    def get(self, id):
        return EnderecoController.buscar_endereco_por_id(id)[0]

    @api.expect(endereco_model, validate=False)
    @api.doc(security='Bearer Auth')
    @jwt_required()
    @autorizacao_endereco
    def put(self, id, endereco):
        data = request.get_json()
        return EnderecoController.atualizar_endereco(endereco, data)

    @api.doc(security='Bearer Auth')
    @jwt_required()
    @autorizacao_endereco
    def delete(self, id, endereco):
        return EnderecoController.deletar_endereco(endereco)
