import uuid
from backend.app.models.ItemCarrinho import ItemCarrinho
from backend.app.models.Carrinho import Carrinho
from backend.app.models.Livro import Livro
from backend.app.db.config import db

class ItemCarrinhoController:

    @staticmethod
    def listar_itens_do_carrinho(id_carrinho):
        itens = ItemCarrinho.query.filter_by(id_carrinho=id_carrinho).all()
        return [item.to_dict(incluir_detalhes=True) for item in itens], 200

    @staticmethod
    def buscar_item_por_id(id_item):
        item = ItemCarrinho.query.get(id_item)
        if not item:
            return {'mensagem': 'Item do carrinho não encontrado'}, 404
        return item.to_dict(incluir_detalhes=True), 200

    @staticmethod
    def adicionar_item_ao_carrinho(data):
        id_carrinho = data.get('id_carrinho')
        id_livro = data.get('id_livro')

        carrinho = Carrinho.query.get(id_carrinho)
        livro = Livro.query.get(id_livro)

        if not carrinho or not livro:
            return {'mensagem': 'Carrinho ou livro não encontrado'}, 404

        novo_item = ItemCarrinho(
            id=str(uuid.uuid4()),
            id_carrinho=id_carrinho,
            id_livro=id_livro
        )

        db.session.add(novo_item)
        db.session.commit()

        return novo_item.to_dict(incluir_detalhes=True), 201

    @staticmethod
    def deletar_item_do_carrinho(id_item):
        item = ItemCarrinho.query.get(id_item)
        if not item:
            return {'mensagem': 'Item do carrinho não encontrado'}, 404

        item_dict = item.to_dict(incluir_detalhes=True)
        db.session.delete(item)
        db.session.commit()

        return {
            'mensagem': 'Item removido com sucesso!',
            'item': item_dict
        }, 200
 
    @staticmethod
    def atualizar_item_carrinho(id_item, data):
        if not isinstance(data, dict):
            data = data.__dict__ if hasattr(data, '__dict__') else {}

        item = ItemCarrinho.query.get(id_item)
        if not item:
            return {'mensagem': 'Item do carrinho não encontrado'}, 404

        novo_id_livro = data.get('id_livro')
        novo_id_carrinho = data.get('id_carrinho')

        if novo_id_livro:
            livro = Livro.query.get(str(novo_id_livro))
            if not livro:
                return {'mensagem': 'Livro não encontrado'}, 404
            item.id_livro = str(novo_id_livro)

        if novo_id_carrinho:
            carrinho = Carrinho.query.get(str(novo_id_carrinho))
            if not carrinho:
                return {'mensagem': 'Carrinho não encontrado'}, 404
            item.id_carrinho = str(novo_id_carrinho)

        db.session.commit()

        return item.to_dict(incluir_detalhes=True), 200
