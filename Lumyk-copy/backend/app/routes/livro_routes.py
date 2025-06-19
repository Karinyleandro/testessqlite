from flask_restx import Namespace, Resource, fields
from flask import request
from backend.app.controllers import LivroController
from backend.app.middlewares.autorizacao_livro import autorizacao_livro
from flask_jwt_extended import jwt_required

api = Namespace('livros', description='Operações relacionadas a Livros')

# Models compartilhados

autor_model = api.model('AutorResponse', {
    'id': fields.String(description='ID do Autor'),
    'nome': fields.String(description='Nome do Autor'),
    'biografia': fields.String(description='Biografia do Autor'),
    'foto': fields.String(description='URL da foto do Autor')
})

genero_model = api.model('GeneroResponse', {
    'id': fields.String(description='ID do Gênero'),
    'nome': fields.String(description='Nome do Gênero'),
})

estado_model = api.model('EstadoResponse', {
    'id': fields.String(description='ID do Estado'),
    'nome': fields.String(description='Nome do Estado'),
})

usuario_model = api.model('UsuarioResponse', {
    'id': fields.String(description='ID do Usuário'),
    'nome': fields.String(description='Nome do Usuário'),
})

endereco_model = api.model('EnderecoResponse', {
    'id': fields.String(description='ID do Endereço'),
    'id_usuario': fields.String(description='ID do Usuário'),
    'id_estado': fields.String(description='ID do Estado'),
    'numero': fields.Integer(description='Número'),
    'bairro': fields.String(description='Bairro'),
    'rua': fields.String(description='Rua'),
})

# Model de entrada (criação e atualização de livros)
livro_model = api.model('Livro', {
    'id_genero': fields.String(required=True, description='ID do Gênero'),
    'id_autor': fields.String(required=True, description='ID do Autor'),
    'foto': fields.String(required=True, description='Foto do Livro'),
    'sinopse': fields.String(required=True, description='Sinopse do Livro'),
    'estoque': fields.Integer(required=True, description='Quantidade em Estoque'),
    'preco': fields.Float(required=True, description='Preço do Livro'),
    'formato': fields.String(required=True, description='Formato do Livro'),
    'tipo': fields.String(required=True, description='Tipo do Livro'),
    'titulo': fields.String(required=True, description='Título do Livro'),
    'id_estado': fields.String(description='ID do Estado'),
    'id_usuario': fields.String(description='ID do Usuário'),
    'id_endereco': fields.String(description='ID do Endereço')
})

# Model de resposta (quando retorna o livro com os relacionamentos completos)
livro_response = api.model('LivroResponse', {
    'id': fields.String(description='ID do Livro'),
    'id_genero': fields.String(description='ID do Gênero'),
    'genero': fields.Nested(genero_model, description='Informações do Gênero'),
    'id_autor': fields.String(description='ID do Autor'),
    'autor': fields.Nested(autor_model, description='Informações do Autor'),
    'id_estado': fields.String(description='ID do Estado'),
    'estado': fields.Nested(estado_model, description='Informações do Estado'),
    'id_usuario': fields.String(description='ID do Usuário'),
    'usuario': fields.Nested(usuario_model, description='Informações do Usuário'),
    'id_endereco': fields.String(description='ID do Endereço'),
    'endereco': fields.Nested(endereco_model, description='Informações do Endereço'),
    'foto': fields.String(description='Foto do Livro'),
    'sinopse': fields.String(description='Sinopse do Livro'),
    'estoque': fields.Integer(description='Quantidade em Estoque'),
    'preco': fields.Float(description='Preço do Livro'),
    'formato': fields.String(description='Formato do Livro'),
    'tipo': fields.String(description='Tipo do Livro'),
    'titulo': fields.String(description='Título do Livro'),
})

# Rotas

@api.route('/')
class LivroList(Resource):
    @api.marshal_list_with(livro_response)
    def get(self):
        return LivroController.listar_livros()[0]

    @jwt_required()
    @api.expect(livro_model)
    @api.response(201, 'Livro criado com sucesso!')
    def post(self):
        data = request.get_json()
        return LivroController.criar_livro(data)

@api.route('/<string:id>')
@api.param('id', 'ID do livro')
class LivroResource(Resource):
    @api.marshal_with(livro_response)
    def get(self, id):
        return LivroController.buscar_livro_por_id(id)[0]

    @jwt_required()
    @autorizacao_livro
    @api.expect(livro_model)
    @api.response(200, 'Livro atualizado com sucesso!')
    def put(self, id):
        data = request.get_json()
        return LivroController.atualizar_livro(id, data)

    @jwt_required()
    @autorizacao_livro
    @api.response(200, 'Livro deletado com sucesso!')
    def delete(self, id):
        return LivroController.deletar_livro(id)
