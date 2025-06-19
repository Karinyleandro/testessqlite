import uuid
from backend.app.db.config import db
from sqlalchemy.orm import relationship


class Assinatura(db.Model):
    __tablename__ = 'Assinatura'

    # o id coloquei em string porque tô usando o uuid para gerar um id único ele é dado em: c3c42be5-ca13-4a58-89a1-80d0f3775026
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey('Usuario.id', ondelete='CASCADE', name='fk_assinatura_usuario'),
        nullable=False
    )

    tipo_assinatura = db.Column(db.String(40), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(40), nullable=False)
    preco_assinatura = db.Column(db.Float, nullable=False)
    
    # Relacionamento com Usuario
    usuario = relationship('Usuario', backref='assinaturas')

    def to_dict(self):
        return {
            "id": self.id,
            "id_usuario": self.id_usuario,
            "usuario": {
                "id": self.usuario.id,
                "nome": self.usuario.nome
            } if self.usuario else None,
            "tipo_assinatura": self.tipo_assinatura,
            "data_inicio": self.data_inicio.isoformat(),
            "data_fim": self.data_fim.isoformat(),
            "status": self.status,
            "preco_assinatura": self.preco_assinatura
        }