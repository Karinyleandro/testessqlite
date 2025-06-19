import uuid
from backend.app.models.ItemPedido import ItemPedido
from backend.app.models.Pedido import Pedido
from backend.app.models.Livro import Livro
from backend.app.db.config import db

class ItemPedidoController:

    @staticmethod
    def listar_itens_do_pedido(id_pedido):
        itens = ItemPedido.query.filter_by(id_pedido=id_pedido).all()
        return [item.to_dict() for item in itens], 200

    @staticmethod
    def buscar_item_por_id(id_item):
        item = ItemPedido.query.get(id_item)
        if not item:
            return {'mensagem': 'Item do pedido não encontrado'}, 404
        return item.to_dict(), 200

    @staticmethod
    def adicionar_item_ao_pedido(data):
        id_pedido = data.get('id_pedido')
        id_livro = data.get('id_livro')
        preco_unitario = data.get('preco_unitario')
        quantidade = data.get('quantidade')

        pedido = Pedido.query.get(id_pedido)
        livro = Livro.query.get(id_livro)

        if not pedido or not livro:
            return {'mensagem': 'Pedido ou livro não encontrado'}, 404

        novo_item = ItemPedido(
            id=str(uuid.uuid4()),
            id_pedido=id_pedido,
            id_livro=id_livro,
            preco_unitario=preco_unitario,
            quantidade=quantidade
        )

        db.session.add(novo_item)
        db.session.commit()

        return novo_item.to_dict(), 201

    @staticmethod
    def deletar_item_do_pedido(id_item):
        item = ItemPedido.query.get(id_item)
        if not item:
            return {'mensagem': 'Item do pedido não encontrado'}, 404

        item_dict = item.to_dict()
        db.session.delete(item)
        db.session.commit()

        return {'mensagem': 'Item removido com sucesso!', 'item': item_dict}, 200

    @staticmethod
    def atualizar_item_pedido(id_item, data):
        if not isinstance(data, dict):
            data = data.__dict__ if hasattr(data, '__dict__') else {}

        item = ItemPedido.query.get(id_item)
        if not item:
            return {'mensagem': 'Item do pedido não encontrado'}, 404

        novo_id_pedido = data.get('id_pedido')
        novo_id_livro = data.get('id_livro')
        preco_unitario = data.get('preco_unitario')
        quantidade = data.get('quantidade')

        if novo_id_pedido:
            pedido = Pedido.query.get(str(novo_id_pedido))
            if not pedido:
                return {'mensagem': 'Pedido não encontrado'}, 404
            item.id_pedido = str(novo_id_pedido)

        if novo_id_livro:
            livro = Livro.query.get(str(novo_id_livro))
            if not livro:
                return {'mensagem': 'Livro não encontrado'}, 404
            item.id_livro = str(novo_id_livro)

        if preco_unitario is not None:
            item.preco_unitario = preco_unitario

        if quantidade is not None:
            item.quantidade = quantidade

        db.session.commit()

        return item.to_dict(), 200
