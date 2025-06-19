from backend.app.models.Livro import Livro
from backend.app.models.GeneroLivro import GeneroLivro
from backend.app.models.Autor import Autor
from backend.app.models.Estado import Estado
from backend.app.models.Usuario import Usuario
from backend.app.models.Endereco import Endereco
from backend.app.db.config import db

def listar_livros():
    livros = Livro.query.all()
    return [livro.to_dict() for livro in livros], 200

def buscar_livro_por_id(id):
    livro = Livro.query.get_or_404(id)
    return livro.to_dict(), 200

def criar_livro(data):
    # Buscar os objetos relacionados a partir dos IDs fornecidos na requisição
    genero = GeneroLivro.query.get(data['id_genero'])
    autor = Autor.query.get(data['id_autor'])
    estado = Estado.query.get(data.get('id_estado'))
    usuario = Usuario.query.get(data.get('id_usuario'))
    endereco = Endereco.query.get(data.get('id_endereco'))

    # Verificar se os relacionamentos existem
    if not genero or not autor:
        return {'mensagem': 'Gênero ou Autor não encontrado'}, 404

    livro = Livro(
        id_genero=genero.id,
        id_autor=autor.id,
        id_estado=estado.id if estado else None,
        id_usuario=usuario.id if usuario else None,
        id_endereco=endereco.id if endereco else None,
        foto=data['foto'],
        sinopse=data['sinopse'],
        estoque=data['estoque'],
        preco=data['preco'],
        formato=data['formato'],
        tipo=data['tipo'],
        titulo=data['titulo']
    )

    db.session.add(livro)
    db.session.commit()
    return livro.to_dict(), 201


def atualizar_livro(id, data):
    livro = Livro.query.get_or_404(id)

    # Atualiza os campos do livro com os dados fornecidos
    livro.id_genero = data.get('id_genero', livro.id_genero)
    livro.id_autor = data.get('id_autor', livro.id_autor)
    livro.foto = data.get('foto', livro.foto)
    livro.sinopse = data.get('sinopse', livro.sinopse)
    livro.estoque = data.get('estoque', livro.estoque)
    livro.preco = data.get('preco', livro.preco)
    livro.formato = data.get('formato', livro.formato)
    livro.tipo = data.get('tipo', livro.tipo)
    livro.titulo = data.get('titulo', livro.titulo)

    # Atualiza o relacionamento com Estado, Usuario, Endereco
    livro.id_estado = data.get('id_estado', livro.id_estado)
    livro.id_usuario = data.get('id_usuario', livro.id_usuario)
    livro.id_endereco = data.get('id_endereco', livro.id_endereco)

    db.session.commit()
    return {'mensagem': 'Livro atualizado com sucesso!', 'livro': livro.to_dict()}, 200

def deletar_livro(id):
    livro = Livro.query.get_or_404(id)
    db.session.delete(livro)
    db.session.commit()
    return {'mensagem': 'Livro deletado com sucesso!'}, 200
