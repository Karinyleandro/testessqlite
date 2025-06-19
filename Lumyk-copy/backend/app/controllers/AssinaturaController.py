import uuid
from flask_jwt_extended import get_jwt_identity
from backend.app.models.Assinatura import Assinatura
from datetime import datetime
from backend.app.db.config import db

def listar_assinaturas():
    id_usuario = get_jwt_identity()
    assinaturas = Assinatura.query.filter_by(id_usuario=id_usuario).all()
    return [a.to_dict() for a in assinaturas], 200

def buscar_assinatura_por_id(id_assinatura):
    id_usuario = get_jwt_identity()
    assinatura = Assinatura.query.get(id_assinatura)
    if not assinatura:
        return {'mensagem': 'Assinatura não encontrada.'}, 404
    if assinatura.id_usuario != id_usuario:
        return {'mensagem': 'Acesso negado: esta assinatura não pertence a você.'}, 403
    return assinatura.to_dict(), 200

def criar_assinatura(data):
    id_usuario = get_jwt_identity()
    try:
        data_inicio = datetime.strptime(data.get('data_inicio'), '%Y-%m-%d').date()
        data_fim = datetime.strptime(data.get('data_fim'), '%Y-%m-%d').date()

        nova_assinatura = Assinatura(
            id=str(uuid.uuid4()),
            id_usuario=id_usuario,
            tipo_assinatura=data.get('tipo_assinatura'),
            data_inicio=data_inicio,
            data_fim=data_fim,
            status=data.get('status'),
            preco_assinatura=data.get('preco_assinatura')
        )
        db.session.add(nova_assinatura)
        db.session.commit()
        return {'mensagem': 'Assinatura criada com sucesso!', 'assinatura': nova_assinatura.to_dict()}, 201
    except Exception as e:
        db.session.rollback()
        return {'mensagem': f'Erro ao criar assinatura: {str(e)}'}, 500

def atualizar_assinatura(id_assinatura, data):
    id_usuario = get_jwt_identity()
    assinatura = Assinatura.query.get(id_assinatura)
    if not assinatura:
        return {'mensagem': 'Assinatura não encontrada.'}, 404
    if assinatura.id_usuario != id_usuario:
        return {'mensagem': 'Acesso negado: esta assinatura não pertence a você.'}, 403

    if 'data_inicio' in data:
        assinatura.data_inicio = datetime.strptime(data['data_inicio'], '%Y-%m-%d').date()
    if 'data_fim' in data:
        assinatura.data_fim = datetime.strptime(data['data_fim'], '%Y-%m-%d').date()

    assinatura.tipo_assinatura = data.get('tipo_assinatura', assinatura.tipo_assinatura)
    assinatura.status = data.get('status', assinatura.status)
    assinatura.preco_assinatura = data.get('preco_assinatura', assinatura.preco_assinatura)

    db.session.commit()
    return {'mensagem': 'Assinatura atualizada com sucesso!', 'assinatura': assinatura.to_dict()}, 200

def deletar_assinatura(id_assinatura):
    id_usuario = get_jwt_identity()
    assinatura = Assinatura.query.get(id_assinatura)
    if not assinatura:
        return {'mensagem': 'Assinatura não encontrada.'}, 404
    if assinatura.id_usuario != id_usuario:
        return {'mensagem': 'Acesso negado: esta assinatura não pertence a você.'}, 403

    db.session.delete(assinatura)
    db.session.commit()
    return {'mensagem': 'Assinatura deletada com sucesso!'}, 200
