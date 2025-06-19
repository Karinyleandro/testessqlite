import uuid
from flask_jwt_extended import get_jwt_identity
from backend.app.models.Autor import Autor
from backend.app.db.config import db

def listar_autores():
    autores = Autor.query.all()
    return [autor.to_dict() for autor in autores], 200

def buscar_autor_por_id(id):
    autor = Autor.query.get_or_404(id)
    return autor.to_dict(), 200

def criar_autor(data):
    usuario_id = get_jwt_identity()

    novo_autor = Autor(
        id=str(uuid.uuid4()),
        nome=data['nome'],
        biografia=data['biografia'],
        foto=data['foto']
    )
    db.session.add(novo_autor)
    db.session.commit()
    return novo_autor.to_dict(), 201


def atualizar_autor(id, data):
    autor = Autor.query.get_or_404(id)

    autor.nome = data.get('nome', autor.nome)
    autor.biografia = data.get('biografia', autor.biografia)
    autor.foto = data.get('foto', autor.foto)

    db.session.commit()
    return {'mensagem': 'Autor atualizado com sucesso!', 'autor': autor.to_dict()}, 200

def deletar_autor(id):
    autor = Autor.query.get_or_404(id)
    db.session.delete(autor)
    db.session.commit()
    return {'mensagem': 'Autor deletado com sucesso!'}, 200
