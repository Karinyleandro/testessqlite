import uuid
from backend.app.db.config import db

class Usuario(db.Model):
    __tablename__ = 'Usuario'

    # o id coloquei em string porque tô usando o uuid para gerar um id único ele é dado em: c3c42be5-ca13-4a58-89a1-80d0f3775026
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    senha = db.Column(db.String(8), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)

    def to_dict(self):
        return{
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,  # nao pode retornar a senha
            "data_nascimento": self.data_nascimento.isoformat()
        }
