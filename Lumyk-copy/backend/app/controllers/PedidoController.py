import uuid
from flask_jwt_extended import get_jwt_identity
from backend.app.models.Pedido import Pedido
from backend.app.models.Estado import Estado
from datetime import datetime
from backend.app.db.config import db

def listar_pedidos():
    id_usuario = get_jwt_identity()
    pedidos = Pedido.query.filter_by(id_usuario=id_usuario).all()
    return [p.to_dict() for p in pedidos], 200

def buscar_pedido_por_id(id_pedido):
    id_usuario = get_jwt_identity()
    pedido = Pedido.query.get(id_pedido)
    if not pedido:
        return {'mensagem': 'Pedido não encontrado.'}, 404
    if pedido.id_usuario != id_usuario:
        return {'mensagem': 'Acesso negado: este pedido não pertence a você.'}, 403
    return pedido.to_dict(), 200

def criar_pedido(data, id_usuario):
    campos_obrigatorios = ['id_endereco', 'total', 'data_compra', 'id_estado']
    faltando = [campo for campo in campos_obrigatorios if not data.get(campo)]
    if faltando:
        return {'mensagem': f'Campos obrigatórios ausentes: {", ".join(faltando)}'}, 400

    # Validar se o estado existe
    estado = None
    if data.get('id_estado'):
        estado = Estado.query.get(data.get('id_estado'))
        if not estado:
            return {'mensagem': 'Estado inválido.'}, 400

    try:
        data_compra_str = data.get('data_compra')
        data_compra = datetime.strptime(data_compra_str, '%Y-%m-%d').date()

        novo_pedido = Pedido(
            id=str(uuid.uuid4()),
            id_usuario=id_usuario,
            id_endereco=data.get('id_endereco'),
            id_pagamento=data.get('id_pagamento'),
            total=data.get('total'),
            data_compra=data_compra,
            id_estado=data.get('id_estado')  # Aqui você garante que o estado seja válido
        )
        db.session.add(novo_pedido)
        db.session.commit()
        return {'mensagem': 'Pedido criado com sucesso!', 'pedido': novo_pedido.to_dict()}, 201
    except Exception as e:
        db.session.rollback()
        return {'mensagem': f'Erro ao criar pedido: {str(e)}'}, 500

def atualizar_pedido(id_pedido, data):
    id_usuario = get_jwt_identity()
    pedido = Pedido.query.get(id_pedido)
    if not pedido:
        return {'mensagem': 'Pedido não encontrado.'}, 404
    if pedido.id_usuario != id_usuario:
        return {'mensagem': 'Acesso negado: este pedido não pertence a você.'}, 403

    if not any(data.get(campo) is not None for campo in ['id_endereco', 'id_pagamento', 'total', 'data_compra', 'id_estado']):
        return {'mensagem': 'Nenhum dado fornecido para atualizar.'}, 400

    try:
        if data.get('data_compra'):
            pedido.data_compra = datetime.strptime(data['data_compra'], '%Y-%m-%d').date()
        if data.get('id_endereco') is not None:
            pedido.id_endereco = data['id_endereco']
        if 'id_pagamento' in data:
            pedido.id_pagamento = data['id_pagamento']
        if data.get('total') is not None:
            pedido.total = data['total']
        if data.get('id_estado') is not None:
            pedido.id_estado = data['id_estado']  # Atualizando o estado

        db.session.commit()
        return {'mensagem': 'Pedido atualizado com sucesso!', 'pedido': pedido.to_dict()}, 200
    except Exception as e:
        db.session.rollback()
        return {'mensagem': f'Erro ao atualizar pedido: {str(e)}'}, 500

def deletar_pedido(id_pedido):
    id_usuario = get_jwt_identity()
    pedido = Pedido.query.get(id_pedido)
    if not pedido:
        return {'mensagem': 'Pedido não encontrado.'}, 404
    if pedido.id_usuario != id_usuario:
        return {'mensagem': 'Acesso negado: este pedido não pertence a você.'}, 403

    try:
        db.session.delete(pedido)
        db.session.commit()
        return {'mensagem': 'Pedido deletado com sucesso!'}, 200
    except Exception as e:
        db.session.rollback()
        return {'mensagem': f'Erro ao deletar pedido: {str(e)}'}, 500
