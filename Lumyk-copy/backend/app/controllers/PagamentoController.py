import uuid
from backend.app.models.Pagamento import Pagamento
from backend.app.db.config import db

def listar_pagamentos():
    pagamentos = Pagamento.query.all()
    return [p.to_dict() for p in pagamentos], 200

def buscar_pagamento_por_id(id_pagamento):
    pagamento = Pagamento.query.get(id_pagamento)
    if not pagamento:
        return {'mensagem': 'Pagamento não encontrado.'}, 404
    return pagamento.to_dict(), 200

def criar_pagamento(data):
    forma_pagamento = data.get('forma_pagamento')
    if not forma_pagamento:
        return {'mensagem': 'A forma de pagamento é obrigatória.'}, 400

    novo_pagamento = Pagamento(
        id=str(uuid.uuid4()),
        forma_pagamento=forma_pagamento
    )
    db.session.add(novo_pagamento)
    db.session.commit()
    return {'mensagem': 'Pagamento criado com sucesso!', 'pagamento': novo_pagamento.to_dict()}, 201

def atualizar_pagamento(id_pagamento, data):
    pagamento = Pagamento.query.get(id_pagamento)
    if not pagamento:
        return {'mensagem': 'Pagamento não encontrado.'}, 404

    forma_pagamento = data.get('forma_pagamento')
    if forma_pagamento:
        pagamento.forma_pagamento = forma_pagamento
        db.session.commit()
        return {'mensagem': 'Pagamento atualizado com sucesso!', 'pagamento': pagamento.to_dict()}, 200
    return {'mensagem': 'Nenhum dado para atualizar.'}, 400

def deletar_pagamento(id_pagamento):
    pagamento = Pagamento.query.get(id_pagamento)
    if not pagamento:
        return {'mensagem': 'Pagamento não encontrado.'}, 404

    db.session.delete(pagamento)
    db.session.commit()
    return {'mensagem': 'Pagamento deletado com sucesso!'}, 200