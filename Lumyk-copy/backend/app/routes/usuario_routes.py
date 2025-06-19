from flask_restx import Namespace, Resource, fields
from flask import request
from backend.app.controllers import UsuarioController
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('usuarios', description='Operações relacionadas a usuários')

# Modelos
usuario_model = api.model('Usuario', {
    'nome': fields.String(required=True),
    'email': fields.String(required=True),
    'senha': fields.String(required=True),
    'data_nascimento': fields.String(required=True, description='Formato: YYYY-MM-DD')
})

recuperar_senha_model = api.model('RecuperarSenha', {
    'email': fields.String(required=True, description="E-mail do usuário para recuperação de senha")
})

atualizar_senha_model = api.model('AtualizarSenha', {
    'codigo': fields.String(required=True),
    'new_password': fields.String(required=True),
    'confirm_password': fields.String(required=True)
})

# Listar todos usuários
@api.route('/')
class ListarUsuarios(Resource):
    @api.doc(description="Listar todos os usuários")
    def get(self):
        return UsuarioController.listar_usuarios()

# Buscar usuário por ID
@api.route('/<string:id>')
class BuscarUsuarioPorId(Resource):
    @api.doc(description="Buscar usuário por ID")
    def get(self, id):
        return UsuarioController.buscar_usuario_por_id(id)

# Atualizar usuário
@api.route('/<string:id>/atualizar')
class AtualizarUsuario(Resource):
    @api.expect(usuario_model)
    @api.doc(description="Atualizar um usuário por ID")
    @jwt_required()  # Exige autenticação com JWT
    def put(self, id):
        # Obtém o ID do usuário autenticado a partir do JWT
        usuario_id_token = get_jwt_identity()

        # Verifica se o ID do usuário autenticado corresponde ao ID passado na URL
        if usuario_id_token != id:
            return {'mensagem': 'Ação não autorizada!'}, 403

        # Se os IDs coincidirem, realiza a atualização
        return UsuarioController.atualizar_usuario(id, request.json)


# Deletar usuário
@api.route('/<string:id>/deletar')
class DeletarUsuario(Resource):
    @api.doc(description="Deletar um usuário por ID")
    @jwt_required()
    def delete(self, id):
        usuario_id_token = get_jwt_identity()
        if usuario_id_token != id:
            return {'mensagem': 'Ação não autorizada!'}, 403
        return UsuarioController.deletar_usuario(id)

# Recuperar senha
@api.route('/recuperar_senha')
class RecuperarSenha(Resource):
    @api.expect(recuperar_senha_model)
    @api.doc(description="Recuperar senha através de e-mail")
    def post(self):
        data = request.get_json()
        return UsuarioController.recuperar_senha(data)

# Atualizar senha após recuperação
@api.route('/atualizar_senha')
class AtualizarSenha(Resource):
    @api.expect(atualizar_senha_model)
    @api.doc(description="Atualizar senha após recuperar o código por e-mail")
    def put(self):
        data = request.get_json()
        return UsuarioController.atualizar_senha(data)
