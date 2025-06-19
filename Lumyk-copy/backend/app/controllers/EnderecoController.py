import uuid
from backend.app.models.Endereco import Endereco
from backend.app.db.config import db
from flask_jwt_extended import get_jwt_identity


def listar_enderecos():
    enderecos = Endereco.query.all()
    return [endereco.to_dict() for endereco in enderecos], 200


def buscar_endereco_por_id(id):
    endereco = Endereco.query.get_or_404(id)
    return endereco.to_dict(), 200


def criar_endereco(data):
    usuario_id = get_jwt_identity()
    
    if not usuario_id:
            return ({'mensagem': 'Usuário não autenticado.'}), 401


    novo_endereco = Endereco(
        id=str(uuid.uuid4()),
        id_usuario=usuario_id,
        id_estado=data.get('id_estado'),
        numero=data.get('numero'),
        bairro=data.get('bairro'),
        rua=data.get('rua')
    )

    db.session.add(novo_endereco)
    db.session.commit()

    return {
        'mensagem': 'Endereço criado com sucesso!',
        'endereco': novo_endereco.to_dict()
    }, 201


def atualizar_endereco(endereco, data):
    endereco.id_estado = data.get('id_estado', endereco.id_estado)
    endereco.numero = data.get('numero', endereco.numero)
    endereco.bairro = data.get('bairro', endereco.bairro)
    endereco.rua = data.get('rua', endereco.rua)

    db.session.commit()

    return {
        'mensagem': 'Endereço atualizado com sucesso!',
        'endereco': endereco.to_dict()
    }, 200


def deletar_endereco(endereco):
    db.session.delete(endereco)
    db.session.commit()
    return {'mensagem': 'Endereço deletado com sucesso!'}, 200
