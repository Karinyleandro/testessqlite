from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from backend.app.controllers.ItemPedidoController import ItemPedidoController
from backend.app.middlewares.autorizacao_pedido import autorizacao_pedido

api = Namespace('item-pedido', description='Operações relacionadas aos itens de pedido')

pedido_model = api.model('PedidoResumo', {
    'id': fields.String,
    'data_compra': fields.String,
    'total': fields.Float,
    'taxa_frete': fields.Float,
})

item_pedido_model = api.model('ItemPedido', {
    'id_pedido': fields.String(required=True),
    'id_livro': fields.String(required=True),
    'preco_unitario': fields.Float(required=True),
    'quantidade': fields.Integer(required=True),
})

item_pedido_response = api.inherit('ItemPedidoResponse', item_pedido_model, {
    'id': fields.String,
    'pedido': fields.Nested(pedido_model, allow_null=True),
})

@api.route('/<string:id_item>')
class ItemPedidoResource(Resource):
    @jwt_required()
    @api.marshal_with(item_pedido_response)
    def get(self, id_item):
        return ItemPedidoController.buscar_item_por_id(id_item)[0]

    @jwt_required()
    def delete(self, id_item):
        return ItemPedidoController.deletar_item_do_pedido(id_item)

    @jwt_required()
    @api.expect(item_pedido_model)
    def put(self, id_item):
        data = request.get_json()
        return ItemPedidoController.atualizar_item_pedido(id_item, data)

@api.route('/pedido/<string:id_pedido>')
class ItensDoPedidoResource(Resource):
    @jwt_required()
    @autorizacao_pedido
    @api.marshal_list_with(item_pedido_response)
    def get(self, id_pedido):
        return ItemPedidoController.listar_itens_do_pedido(id_pedido)[0]

@api.route('/')
class ItemPedidoListaResource(Resource):
    @jwt_required()
    @api.expect(item_pedido_model)
    def post(self):
        data = request.get_json()
        return ItemPedidoController.adicionar_item_ao_pedido(data)
