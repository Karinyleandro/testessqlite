from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required
from backend.app.controllers import ItemCarrinhoController
from backend.app.middlewares.autorizacao_item_carrinho import autorizacao_carrinho

api = Namespace('item-carrinho', description='Operações relacionadas a Itens do Carrinho')

# Modelo de entrada
item_model = api.model('ItemCarrinho', {
    'id_carrinho': fields.String(required=True, description='ID do carrinho'),
    'id_livro': fields.String(required=True, description='ID do livro')
})

# Modelo de resposta com detalhes
item_response = api.clone('ItemCarrinhoResponse', item_model, {
    'id': fields.String(required=True, description='ID do item'),
    'livro': fields.Raw(description='Detalhes do livro'),
    'carrinho': fields.Raw(description='Detalhes do carrinho')
})

@api.route('/')
class AdicionarItem(Resource):
    @jwt_required()
    @api.expect(item_model)
    @api.marshal_with(item_response, code=201)
    @api.response(400, 'Campos obrigatórios ausentes ou inválidos')
    @api.response(404, 'Carrinho ou livro não encontrado')
    @autorizacao_carrinho
    def post(self, item=None):  # item é injetado pelo middleware
        data = request.get_json()
        return ItemCarrinhoController.adicionar_item_ao_carrinho(data)

@api.route('/<string:id_item>')
@api.param('id_item', 'ID do item do carrinho')
class ItemCarrinhoResource(Resource):
    @jwt_required()
    @api.marshal_with(item_response)
    @api.response(404, 'Item do carrinho não encontrado')
    def get(self, id_item):
        return ItemCarrinhoController.buscar_item_por_id(id_item)

    @jwt_required()
    @api.expect(item_model)
    @api.marshal_with(item_response)
    @api.response(200, 'Item atualizado com sucesso!')
    @api.response(404, 'Item, carrinho ou livro não encontrado')
    @autorizacao_carrinho
    def put(self, id_item, item=None):
        data = request.get_json()
        return ItemCarrinhoController.atualizar_item_carrinho(id_item, data)

    @jwt_required()
    @api.response(200, 'Item removido com sucesso!')
    @api.response(404, 'Item do carrinho não encontrado')
    @autorizacao_carrinho
    def delete(self, id_item):
        return ItemCarrinhoController.deletar_item_do_carrinho(id_item)

@api.route('/carrinho/<string:id_carrinho>')
@api.param('id_carrinho', 'ID do carrinho')
class ItensPorCarrinho(Resource):
    @jwt_required()
    @api.marshal_list_with(item_response)
    def get(self, id_carrinho):
        return ItemCarrinhoController.listar_itens_do_carrinho(id_carrinho)
