from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required
from backend.app.controllers import AssinaturaController
from backend.app.middlewares.autorizacao_assinatura import autorizacao_assinatura

api = Namespace('assinaturas', description='Operações com assinaturas')

assinatura_model = api.model('Assinatura', {
    'tipo_assinatura': fields.String(required=True),
    'data_inicio': fields.String(required=True, description='Formato: YYYY-MM-DD'),
    'data_fim': fields.String(required=True),
    'status': fields.String(required=True),
    'preco_assinatura': fields.Float(required=True),
})

assinatura_response = api.clone('AssinaturaResponse', assinatura_model, {
    'id': fields.String(),
    'id_usuario': fields.String()
})

@api.route('/')
class AssinaturaList(Resource):
    @jwt_required()
    @api.marshal_list_with(assinatura_response)
    def get(self):
        return AssinaturaController.listar_assinaturas()[0]

    @jwt_required()
    @api.expect(assinatura_model)
    @api.response(201, 'Assinatura criada com sucesso!')
    def post(self):
        data = request.get_json()
        return AssinaturaController.criar_assinatura(data)

@api.route('/<string:id_assinatura>')
@api.param('id_assinatura', 'ID da assinatura')
class AssinaturaResource(Resource):
    @jwt_required()
    @autorizacao_assinatura
    @api.marshal_with(assinatura_response)
    def get(self, id_assinatura):
        return AssinaturaController.buscar_assinatura_por_id(id_assinatura)[0]

    @jwt_required()
    @autorizacao_assinatura
    @api.expect(assinatura_model)
    def put(self, id_assinatura):
        data = request.get_json()
        return AssinaturaController.atualizar_assinatura(id_assinatura, data)

    @jwt_required()
    @autorizacao_assinatura
    def delete(self, id_assinatura):
        return AssinaturaController.deletar_assinatura(id_assinatura)
