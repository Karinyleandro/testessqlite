from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify
from backend.app.models.Pagamento import Pagamento

def autorizacao_pagamento(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        id_usuario_logado = get_jwt_identity()
        id_pagamento = kwargs.get('id_pagamento') 

        pagamento = Pagamento.query.get(id_pagamento)

        if not pagamento:
            return jsonify({'mensagem': 'Pagamento não encontrado.'}), 404

        if pagamento.id_usuario != id_usuario_logado:
            return jsonify({'mensagem': 'Acesso negado: este pagamento não pertence a você.'}), 403

        return f(*args, **kwargs)
    
    return wrapper