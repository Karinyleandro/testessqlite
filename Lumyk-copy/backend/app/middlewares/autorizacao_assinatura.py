from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify
from backend.app.models.Assinatura import Assinatura

def autorizacao_assinatura(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        id_usuario_logado = get_jwt_identity()
        id_assinatura = kwargs.get('id_assinatura')

        assinatura = Assinatura.query.get(id_assinatura)
        if not assinatura:
            return jsonify({'mensagem': 'Assinatura não encontrada.'}), 404

        if assinatura.id_usuario != id_usuario_logado:
            return jsonify({'mensagem': 'Acesso negado: esta assinatura não pertence a você.'}), 403

        return f(*args, **kwargs)
    
    return wrapper