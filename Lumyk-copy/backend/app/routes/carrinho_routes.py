from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required
from backend.app.controllers import CarrinhoController
from backend.app.middlewares.autorizacao_carrinho import autorizacao_carrinho

api = Namespace('carrinhos', description='Operações relacionadas a Carrinhos')

carrinho_model = api.model('Carrinho', {
    'data_criacao': fields.String(required=True, description='Data de criação no formato YYYY-MM-DD'),
})

carrinho_response = api.clone('CarrinhoResponse', carrinho_model, {
    'id': fields.String(required=True, description='ID do carrinho'),
    'id_usuario': fields.String(required=True, description='ID do usuário dono do carrinho'),
})

@api.route('/')
class CarrinhoList(Resource):
    @jwt_required()
    @api.marshal_list_with(carrinho_response)
    def get(self):
        return CarrinhoController.listar_carrinhos()[0]

    @jwt_required()
    @api.expect(carrinho_model)
    @api.response(201, 'Carrinho criado com sucesso!')
    def post(self):
        data = request.get_json()
        return CarrinhoController.criar_carrinho(data)

@api.route('/<string:id_carrinho>')
@api.param('id_carrinho', 'ID do carrinho')
class CarrinhoResource(Resource):
    @jwt_required()
    @api.marshal_with(carrinho_response)
    def get(self, id_carrinho):
        return CarrinhoController.buscar_por_id(id_carrinho)[0]

    @jwt_required()
    @autorizacao_carrinho
    @api.expect(carrinho_model)
    def put(self, id_carrinho, carrinho=None):
        data = request.get_json()
        return CarrinhoController.atualizar_carrinho(id_carrinho, data, carrinho)

    @jwt_required()
    @autorizacao_carrinho
    def delete(self, id_carrinho, carrinho=None):
        return CarrinhoController.deletar_carrinho(id_carrinho, carrinho)
