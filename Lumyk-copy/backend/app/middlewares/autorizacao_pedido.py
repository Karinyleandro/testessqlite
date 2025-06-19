from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify, request
from backend.app.models.Pedido import Pedido

def autorizacao_pedido(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        id_usuario_logado = get_jwt_identity()
        id_pedido = kwargs.get('id_pedido') or request.view_args.get('id_pedido')

        if not id_pedido:
            return jsonify({'mensagem': 'ID do pedido não fornecido na URL.'}), 400

        pedido = Pedido.query.get(str(id_pedido))

        if not pedido:
            return jsonify({'mensagem': 'Pedido não encontrado.'}), 404

        if str(pedido.id_usuario) != str(id_usuario_logado):
            return jsonify({'mensagem': 'Acesso negado: este pedido não pertence a você.'}), 403

        return f(*args, **kwargs)

    return wrapper
