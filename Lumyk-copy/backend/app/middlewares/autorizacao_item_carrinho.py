from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import request
from backend.app.models.Carrinho import Carrinho
from backend.app.models.ItemCarrinho import ItemCarrinho

def autorizacao_carrinho(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        metodo = request.method
        id_carrinho = None

        if metodo == 'POST':
            data = request.get_json(silent=True) or {}
            id_carrinho = data.get('id_carrinho')

        elif metodo in ['PUT', 'DELETE']:
            id_item = kwargs.get('id_item')
            if not id_item:
                return {'mensagem': 'ID do item não fornecido.'}, 400
            
            item = ItemCarrinho.query.get(str(id_item))
            if not item:
                return {'mensagem': 'Item do carrinho não encontrado.'}, 404

            id_carrinho = item.id_carrinho

        elif metodo == 'GET':
            # Para listagem, o controller já pega id_usuario via JWT, não precisa validar aqui
            return func(*args, **kwargs)

        if not id_carrinho:
            return {'mensagem': 'ID do carrinho não fornecido.'}, 400

        carrinho = Carrinho.query.get(str(id_carrinho))
        if not carrinho:
            return {'mensagem': 'Carrinho não encontrado.'}, 404

        id_usuario = get_jwt_identity()
        if carrinho.id_usuario != id_usuario:
            return {'mensagem': 'Acesso negado ao carrinho.'}, 403

        return func(*args, **kwargs)

    return wrapper
