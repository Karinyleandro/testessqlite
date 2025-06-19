from backend.app.models.Estado import Estado
from backend.app.db.config import db
import uuid

def listar_estados():
    estados = Estado.query.all()
    return [estado.to_dict() for estado in estados], 200

def buscar_estado_por_id(id):
    estado = Estado.query.get_or_404(id)
    return estado.to_dict(), 200

def criar_estado(data):
    nome = data.get('nome')
    taxa_frete = data.get('taxa_frete')

    if not nome:
        return {'mensagem': 'Nome é obrigatório'}, 400

    if taxa_frete is None:
        return {'mensagem': 'Frete é obrigatório'}, 400

    if Estado.query.filter_by(nome=nome).first():
        return {'mensagem': 'Já existe um estado com esse nome.'}, 400

    novo_estado = Estado(
        id=str(uuid.uuid4()),
        nome=nome,
        taxa_frete=taxa_frete
    )

    db.session.add(novo_estado)
    db.session.commit()
    return {'mensagem': 'Estado criado com sucesso!', 'estado': novo_estado.to_dict()}, 201

def atualizar_estado(id, data):
    estado = Estado.query.get_or_404(id)

    nome = data.get('nome')
    taxa_frete = data.get('taxa_frete')

    if nome:
        if Estado.query.filter(Estado.nome == nome, Estado.id != id).first():
            return {'mensagem': 'Já existe outro estado com esse nome.'}, 400
        estado.nome = nome

    if taxa_frete is not None:
        estado.taxa_frete = taxa_frete

    db.session.commit()
    return {'mensagem': 'Estado atualizado com sucesso!', 'estado': estado.to_dict()}, 200

def deletar_estado(id):
    estado = Estado.query.get_or_404(id)
    db.session.delete(estado)
    db.session.commit()
    return {'mensagem': 'Estado deletado com sucesso!'}, 200