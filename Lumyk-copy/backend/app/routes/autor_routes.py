from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required
from backend.app.controllers import AutorController

api = Namespace('autores', description='Operações relacionadas a Autores')

autor_model = api.model('Autor', {
    'nome': fields.String(required=True, description='Nome do autor'),
    'biografia': fields.String(required=True, description='Biografia do autor'),
    'foto': fields.String(required=True, description='URL da foto do autor'),
})

autor_response = api.clone('AutorResponse', autor_model, {
    'id': fields.String(required=True, description='ID do autor')
})

@api.route('/')
class AutorList(Resource):
    @api.marshal_list_with(autor_response)
    def get(self):
        return AutorController.listar_autores()[0]

    @jwt_required()
    @api.expect(autor_model)
    @api.marshal_with(autor_response)  
    @api.response(201, 'Autor criado com sucesso!')
    def post(self):
        data = request.get_json()
        return AutorController.criar_autor(data)


@api.route('/<string:id>')
@api.param('id', 'ID do autor')
class AutorResource(Resource):
    @jwt_required()
    @api.marshal_with(autor_response)
    def get(self, id):
        return AutorController.buscar_autor_por_id(id)[0]

    @jwt_required()
    @api.expect(autor_model)
    @api.response(200, 'Autor atualizado com sucesso!')
    def put(self, id):
        data = request.get_json()
        return AutorController.atualizar_autor(id, data)

    @jwt_required()
    @api.response(200, 'Autor deletado com sucesso!')
    def delete(self, id):
        return AutorController.deletar_autor(id)
