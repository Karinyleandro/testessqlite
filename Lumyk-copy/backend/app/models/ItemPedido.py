import uuid
from backend.app.db.config import db

class ItemPedido(db.Model):
    __tablename__ = 'ItemPedido'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    id_pedido = db.Column(
        db.String(36),
        db.ForeignKey('Pedido.id', ondelete='CASCADE', name='fk_itempedido_pedido'),
        nullable=False
    )

    id_livro = db.Column(
        db.String(36),
        db.ForeignKey('Livro.id', ondelete='CASCADE', name='fk_itempedido_livro'),
        nullable=False
    )

    preco_unitario = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

    pedido = db.relationship("Pedido", backref="itens", lazy="joined")  # inner join real
    livro = db.relationship("Livro", backref="itens", lazy="joined")    
    
    def to_dict(self):
        return {
            "id": self.id,
            "id_pedido": self.id_pedido,
            "id_livro": self.id_livro,
            "preco_unitario": self.preco_unitario,
            "quantidade": self.quantidade,
            "pedido": {
                "id": self.pedido.id,
                "data_compra": self.pedido.data_compra.isoformat(),
                "total": self.pedido.total,
                "taxa_frete": self.pedido.estado.taxa_frete if self.pedido and self.pedido.estado else None
            } if self.pedido else None,
            "livro": self.livro.to_dict() if self.livro else None
        }
