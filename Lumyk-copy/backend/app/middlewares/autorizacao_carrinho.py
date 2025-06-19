from functools import wraps
from flask_jwt_extended import get_jwt_identity
from backend.app.models.Carrinho import Carrinho

def autorizacao_carrinho(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        id_carrinho = kwargs.get('id_carrinho')
        if not id_carrinho:
            return {'mensagem': 'ID do carrinho não fornecido.'}, 400

        carrinho = Carrinho.query.get(str(id_carrinho))
        if not carrinho:
            return {'mensagem': 'Carrinho não encontrado.'}, 404

        id_usuario = get_jwt_identity()
        if carrinho.id_usuario != id_usuario:
            return {'mensagem': 'Acesso negado ao carrinho.'}, 403

        return func(*args, carrinho=carrinho, **kwargs)

    return wrapper
