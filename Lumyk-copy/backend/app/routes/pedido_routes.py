from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app.controllers import PedidoController
from backend.app.middlewares.autorizacao_pedido import autorizacao_pedido
from flask import make_response
from flask_restx import marshal

api = Namespace('pedidos', description='Operações relacionadas a pedidos')

# Modelos de resumo das entidades relacionadas
usuario_model = api.model('UsuarioResumo', {
    'id': fields.String,
    'nome': fields.String,
})

endereco_model = api.model('EnderecoResumo', {
    'id': fields.String,
    'rua': fields.String,
})

pagamento_model = api.model('PagamentoResumo', {
    'id': fields.String,
    'forma_pagamento': fields.String,
})

estado_model = api.model('EstadoResumo', {
    'id': fields.String,
    'nome': fields.String,
    'taxa_frete': fields.Float
})

# Modelo do pedido
pedido_model = api.model('Pedido', {
    'id_endereco': fields.String(required=True),
    'id_pagamento': fields.String(required=False),
    'total': fields.Float(required=True),
    'data_compra': fields.String(required=True),
    'id_estado': fields.String(required=False)  # Adicionando o campo de estado
})

# Modelo de resposta do pedido, incluindo as entidades relacionadas
pedido_response = api.inherit('PedidoResponse', pedido_model, {
    'id': fields.String,
    'id_usuario': fields.String,
    'usuario': fields.Nested(usuario_model, allow_null=True),
    'endereco': fields.Nested(endereco_model, allow_null=True),
    'pagamento': fields.Nested(pagamento_model, allow_null=True),
    'estado': fields.Nested(estado_model, allow_null=True),  # Adicionando o estado na resposta
})

@api.route('/')
class PedidoList(Resource):
    @jwt_required()
    @api.marshal_list_with(pedido_response)
    def get(self):
        """Listar todos os pedidos do usuário autenticado."""
        return PedidoController.listar_pedidos()[0]

    @jwt_required()
    @api.expect(pedido_model)
    def post(self):
        """Criar um novo pedido."""
        data = request.get_json()
        id_usuario = get_jwt_identity()
        
        # Verificar se os campos obrigatórios estão presentes antes de chamar o controlador
        if not data.get('id_endereco') or not data.get('total') or not data.get('data_compra'):
            return {'mensagem': 'Campos obrigatórios ausentes: id_endereco, total, data_compra.'}, 400

        return PedidoController.criar_pedido(data, id_usuario)

@api.route('/<string:id_pedido>')
@api.param('id_pedido', 'ID do pedido')
class PedidoResource(Resource):
    @jwt_required()
    @autorizacao_pedido
    @api.marshal_with(pedido_response)
    def get(self, id_pedido):
        """Buscar um pedido pelo ID, com autorização."""
        return PedidoController.buscar_pedido_por_id(id_pedido)[0]

    @jwt_required()
    @autorizacao_pedido
    @api.expect(pedido_model)
    def put(self, id_pedido):
        """Atualizar um pedido existente."""
        data = request.get_json()

        # Validar dados antes de chamar o controlador
        if not data.get('id_endereco') and not data.get('total') and not data.get('data_compra') and not data.get('id_estado'):
            return {'mensagem': 'Nenhum dado fornecido para atualização.'}, 400
        
        # Chama o controlador para atualizar o pedido
        return PedidoController.atualizar_pedido(id_pedido, data)

    @jwt_required()
    @autorizacao_pedido
    def delete(self, id_pedido):
        """Deletar um pedido existente."""
        return PedidoController.deletar_pedido(id_pedido)
