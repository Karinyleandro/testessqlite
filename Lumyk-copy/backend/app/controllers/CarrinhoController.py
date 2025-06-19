from backend.app.models.Carrinho import Carrinho
from backend.app.db.config import db
from datetime import datetime, date
from flask_jwt_extended import get_jwt_identity
import uuid

def listar_carrinhos():
    id_usuario = get_jwt_identity()
    carrinhos = Carrinho.query.filter_by(id_usuario=id_usuario).all()
    return [c.to_dict() for c in carrinhos], 200

def buscar_por_id(id_carrinho):
    carrinho = Carrinho.query.get(str(id_carrinho))
    if not carrinho:
        return {'mensagem': 'Carrinho não encontrado.'}, 404
    return carrinho.to_dict(), 200

def criar_carrinho(data):
    try:
        id_usuario = get_jwt_identity()

        # Verifica se o usuário já tem um carrinho
        carrinho_existente = Carrinho.query.filter_by(id_usuario=id_usuario).first()
        if carrinho_existente:
            return {
                'mensagem': 'Você já possui um carrinho.',
                'carrinho': carrinho_existente.to_dict()
            }, 200  

        data_criacao_str = data.get('data_criacao')
        data_criacao = datetime.strptime(data_criacao_str, "%Y-%m-%d").date() if data_criacao_str else date.today()

        novo_carrinho = Carrinho(
            id=str(uuid.uuid4()),
            id_usuario=id_usuario,
            data_criacao=data_criacao
        )

        db.session.add(novo_carrinho)
        db.session.commit()

        return {
            'mensagem': 'Carrinho criado com sucesso!',
            'carrinho': novo_carrinho.to_dict()
        }, 201

    except Exception as e:
        return {
            'mensagem': f'Erro ao criar carrinho: {str(e)}'
        }, 500

def atualizar_carrinho(id_carrinho, data, carrinho):
    try:
        data_criacao_str = data.get('data_criacao')
        if data_criacao_str:
            carrinho.data_criacao = datetime.strptime(data_criacao_str, "%Y-%m-%d").date()
            db.session.commit()
            return {'mensagem': 'Carrinho atualizado com sucesso!', 'carrinho': carrinho.to_dict()}, 200
        return {'mensagem': 'Nada para atualizar'}, 400
    except Exception as e:
        return {'mensagem': f'Erro ao atualizar carrinho: {str(e)}'}, 500

def deletar_carrinho(id_carrinho, carrinho):
    db.session.delete(carrinho)
    db.session.commit()
    return {'mensagem': 'Carrinho deletado com sucesso!'}, 200
