import uuid
from backend.app.db.config import db

class Carrinho(db.Model):
    __tablename__ = 'Carrinho'

    # o id coloquei em string porque tô usando o uuid para gerar um id único ele é dado em: c3c42be5-ca13-4a58-89a1-80d0f3775026
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey('Usuario.id', ondelete='CASCADE', name='fk_carrinho_usuario'),
        nullable=False
    )

    data_criacao = db.Column(db.Date, nullable=False)
    
    # Relacionamento com Usuario
    usuario = db.relationship('Usuario', backref=db.backref('carrinhos', cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            "id": self.id,
            "id_usuario": self.id_usuario,
            "data_criacao": self.data_criacao.isoformat(),
            "usuario": {
                "id": self.usuario.id,
                "nome": self.usuario.nome
            } if self.usuario else None
        }
