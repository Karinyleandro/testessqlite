import uuid
from backend.app.db.config import db

class Livro(db.Model):
    __tablename__ = 'Livro'

    # ID único com UUID
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Foreign Keys
    id_genero = db.Column(
        db.String(36),
        db.ForeignKey('GeneroLivro.id', ondelete='CASCADE', name='fk_livro_genero'),
        nullable=False
    )

    id_autor = db.Column(
        db.String(36),
        db.ForeignKey('Autor.id', ondelete='CASCADE', name='fk_livro_autor'),
        nullable=False
    )
    
    id_estado = db.Column(
        db.String(36),
        db.ForeignKey('Estado.id', ondelete='CASCADE', name='fk_livro_estado'),
        nullable=True
    )

    id_usuario = db.Column(
        db.String(36),
        db.ForeignKey('Usuario.id', ondelete='CASCADE', name='fk_livro_usuario'),
        nullable=True
    )

    id_endereco = db.Column(
        db.String(36),
        db.ForeignKey('Endereco.id', ondelete='CASCADE', name='fk_livro_endereco'),
        nullable=True
    )

    # Atributos do livro
    foto = db.Column(db.Text, nullable=False)
    sinopse = db.Column(db.String(350), nullable=False)
    estoque = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    formato = db.Column(db.String(40), nullable=False)
    tipo = db.Column(db.String(40), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)

    # Relacionamentos
    genero = db.relationship('GeneroLivro', backref=db.backref('livros', cascade='all, delete-orphan'))
    autor = db.relationship('Autor', backref=db.backref('livros', cascade='all, delete-orphan'))
    estado = db.relationship('Estado', backref=db.backref('livros', cascade='all, delete-orphan'))
    usuario = db.relationship('Usuario', backref=db.backref('livros', cascade='all, delete-orphan'))
    endereco = db.relationship('Endereco', backref=db.backref('livros', cascade='all, delete-orphan'))
    
    

    # Método para transformar em dicionário (JSON-friendly)
    def to_dict(self):
        return {
            "id": self.id,
            "id_genero": self.id_genero,
            "id_autor": self.id_autor,
            "id_estado": self.id_estado,
            "id_usuario": self.id_usuario,
            "id_endereco": self.id_endereco,
            "foto": self.foto,
            "sinopse": self.sinopse,
            "estoque": self.estoque,
            "preco": self.preco,
            "formato": self.formato,
            "tipo": self.tipo,
            "titulo": self.titulo,
            "genero": {
                "id": self.genero.id,
                "nome": self.genero.nome
            } if self.genero else None,
            "autor": {
                "id": self.autor.id,
                "nome": self.autor.nome,
                "biografia": self.autor.biografia,
                "foto": self.autor.foto
            } if self.autor else None,
            "estado": {
                "id": self.estado.id,
                "nome": self.estado.nome
            } if self.estado else None,
            "usuario": {
                "id": self.usuario.id,
                "nome": self.usuario.nome
            } if self.usuario else None,
            "endereco": {
                "id": self.endereco.id,
                "rua": self.endereco.rua,
                "bairro": self.endereco.bairro,
                "numero": self.endereco.numero
            } if self.endereco else None
        }
