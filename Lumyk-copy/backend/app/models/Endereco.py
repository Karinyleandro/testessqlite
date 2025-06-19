import uuid 
from backend.app.db.config import db

class Endereco(db.Model):
    __tablename__ = 'Endereco'

    # o id coloquei em string porque tô usando o uuid para gerar um id único ele é dado em: c3c42be5-ca13-4a58-89a1-80d0f3775026
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    id_usuario = db.Column(
        db.String(36),
        db.ForeignKey('Usuario.id', ondelete='CASCADE', name='fk_endereco_usuario'),
        nullable=False
    )

    id_estado = db.Column(
        db.String(36),
        db.ForeignKey('Estado.id', ondelete='CASCADE', name='fk_endereco_estado'),
        nullable=True
    )

    numero = db.Column(db.Integer, nullable=True)
    bairro = db.Column(db.String(40), nullable=True)
    rua = db.Column(db.String(100), nullable=True)
    
    # Relacionamentos
    usuario = db.relationship('Usuario', backref='enderecos', lazy=True)
    estado = db.relationship('Estado', backref='enderecos', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "id_usuario": self.id_usuario,
            "usuario": {
                "id": self.usuario.id,
                "nome": self.usuario.nome
            } if self.usuario else None,

            "id_estado": self.id_estado,
            "estado": {
                "id": self.estado.id,
                "nome": self.estado.nome
            } if self.estado else None,

            "numero": self.numero,
            "bairro": self.bairro,
            "rua": self.rua
        }