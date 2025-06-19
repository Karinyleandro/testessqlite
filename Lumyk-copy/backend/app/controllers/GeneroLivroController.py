import uuid
from backend.app.models.GeneroLivro import GeneroLivro
from backend.app.db.config import db

def listar_generos():
    generos = GeneroLivro.query.all()
    return [genero.to_dict() for genero in generos], 200

def buscar_genero_por_id(id):
    genero = GeneroLivro.query.get_or_404(id)
    return genero.to_dict(), 200

def criar_genero(data):
    if GeneroLivro.query.filter_by(nome=data['nome']).first():
        return {'mensagem': 'Gênero já existe.'}, 400

    novo_genero = GeneroLivro(
        id=str(uuid.uuid4()),
        nome=data['nome']
    )
    db.session.add(novo_genero)
    db.session.commit()
    return {'mensagem': 'Gênero criado com sucesso!', 'genero': novo_genero.to_dict()}, 201

def atualizar_genero(id, data):
    genero = GeneroLivro.query.get_or_404(id)

    if 'nome' in data:
        nome_existente = GeneroLivro.query.filter_by(nome=data['nome']).first()
        if nome_existente and nome_existente.id != id:
            return {'mensagem': 'Já existe um gênero com esse nome.'}, 400
        genero.nome = data['nome']

    db.session.commit()
    return {'mensagem': 'Gênero atualizado com sucesso!', 'genero': genero.to_dict()}, 200

def deletar_genero(id):
    genero = GeneroLivro.query.get_or_404(id)
    db.session.delete(genero)
    db.session.commit()
    return {'mensagem': 'Gênero deletado com sucesso!'}, 200
