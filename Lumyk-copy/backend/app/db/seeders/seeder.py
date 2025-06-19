import sys
import os
import json
from backend.app import db  
from backend.app.models.Autor import Autor
from backend.app.models.GeneroLivro import GeneroLivro
from backend.app.models.Livro import Livro
from backend.app.models.Estado import Estado
from run import create_app

'''
    Se eu quiser rodar usar esse comando aqui:
       $ PYTHONPATH=backend python -m backend.app.db.seeders.seeder
            Autores inseridos com sucesso!
            Gêneros inseridos com sucesso!
            Livros inseridos com sucesso!

'''

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

def carregar_json(nome_arquivo):
    caminho = os.path.join(os.path.dirname(__file__), nome_arquivo)
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)

def seed_autores():
    autores = carregar_json('autores.json')

    for autor in autores:
        novo_autor = Autor(
            nome=autor['nome'],
            biografia=autor['biografia'],
            foto=autor['foto'] if autor['foto'] else None
        )
        db.session.add(novo_autor)

    db.session.commit()
    print("Autores inseridos com sucesso!")

def seed_generos():
    generos = carregar_json('generos.json')

    for genero in generos:
        novo_genero = GeneroLivro(nome=genero['nome'].strip())
        db.session.add(novo_genero)

    db.session.commit()
    print("Gêneros inseridos com sucesso!")

def seed_livros():
    livros = carregar_json('livros.json')  #
    for livro in livros:
        # Buscar o autor pelo nome (pega o ID automaticamente)
        autor = Autor.query.filter_by(nome=livro['id_autor']).first()
        # Buscar o gênero pelo nome (pega o ID automaticamente)
        genero = GeneroLivro.query.filter_by(nome=livro['id_genero']).first()

        if autor and genero:
            novo_livro = Livro(
            titulo=livro['titulo'],
            sinopse=livro['sinopse'],
            preco=float(livro['preco']),
            formato=livro['formato'],
            tipo=livro['tipo'],
            foto=livro['foto'],              
            estoque=int(livro['estoque']),
            id_autor=autor.id,               
            id_genero=genero.id              
        )

            db.session.add(novo_livro)
        else:
            if not autor:
                print(f"Erro ao inserir o livro '{livro['titulo']}': autor '{livro['id_autor']}' não encontrado.")
            if not genero:
                print(f"Erro ao inserir o livro '{livro['titulo']}': gênero '{livro['id_genero']}' não encontrado.")

    db.session.commit()
    print("Livros inseridos com sucesso!")

def seed_estados():
    estados = carregar_json('estados.json')
    
    for estado in estados:
        nome = estado['nome'].strip() 
        taxa_frete = estado['taxa_frete']

        if not nome or taxa_frete is None:
            print(f"Erro no estado: {estado}, nome ou frete faltando!")
            continue 
        novo_estado = Estado(nome=nome, taxa_frete=taxa_frete)
        db.session.add(novo_estado)

    db.session.commit()
    print("Estados inseridos com sucesso!")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_autores()
        seed_generos()
        seed_livros()
        seed_estados()
