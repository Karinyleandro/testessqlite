from functools import wraps
from flask_jwt_extended import get_jwt_identity
from backend.app.models.Endereco import Endereco

def autorizacao_endereco(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        id_endereco = kwargs.get('id')
        if not id_endereco:
            return {'mensagem': 'ID do endereço não fornecido.'}, 400

        endereco = Endereco.query.get(str(id_endereco))
        if not endereco:
            return {'mensagem': 'Endereço não encontrado.'}, 404

        usuario_id = get_jwt_identity()
        if str(endereco.id_usuario) != str(usuario_id):
            return {'mensagem': 'Você não tem permissão para acessar este endereço.'}, 403

        return func(*args, endereco=endereco, **kwargs)

    return wrapper
