from flask_restx import Namespace, Resource, fields
from flask import request
from backend.app.controllers import GeneroLivroController
from flask_jwt_extended import jwt_required

api = Namespace('generos', description='Operações relacionadas a Gêneros de Livros')

genero_model = api.model('GeneroLivro', {
    'nome': fields.String(required=True, description='Nome do gênero'),
})

genero_response = api.clone('GeneroLivroResponse', genero_model, {
    'id': fields.String(required=True, description='ID do gênero')
})

@api.route('/')
class GeneroList(Resource):
    @api.marshal_list_with(genero_response)
    def get(self):
        return GeneroLivroController.listar_generos()[0]

    @jwt_required()
    @api.expect(genero_model)
    @api.response(201, 'Gênero criado com sucesso!')
    @api.response(400, 'Gênero já existe.')
    def post(self):
        data = request.get_json()
        return GeneroLivroController.criar_genero(data)

@api.route('/<string:id>')
@api.param('id', 'ID do gênero')
class GeneroResource(Resource):
    @api.marshal_with(genero_response)
    def get(self, id):
        return GeneroLivroController.buscar_genero_por_id(id)[0]

    @jwt_required()
    @api.expect(genero_model)
    @api.response(200, 'Gênero atualizado com sucesso!')
    @api.response(400, 'Nome de gênero já existe.')
    def put(self, id):
        data = request.get_json()
        return GeneroLivroController.atualizar_genero(id, data)

    @jwt_required() 
    @api.response(200, 'Gênero deletado com sucesso!')
    def delete(self, id):
        return GeneroLivroController.deletar_genero(id)
