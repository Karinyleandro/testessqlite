import uuid
from backend.app.db.config import db

class GeneroLivro(db.Model):
    __tablename__ = 'GeneroLivro'
    
    # o id coloquei em string porque tô usando o uuid para gerar um id único ele é dado em: c3c42be5-ca13-4a58-89a1-80d0f3775026
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = db.Column(db.String(40), unique=True, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome
        }