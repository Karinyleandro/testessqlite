import bcrypt
import jwt
import uuid
from flask import current_app
from datetime import datetime, timedelta
from backend.app.db.config import db
from backend.app.models.Usuario import Usuario

def registrar_usuario(data):  
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    data_nascimento_str = data.get('data_nascimento')

    if not nome or not email or not senha or not data_nascimento_str:
        return {'mensagem': 'Todos os campos são obrigatórios (nome, email, senha, data_nascimento)!'}, 400

    try:
        data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d')
    except ValueError:
        return {'mensagem': 'Data de nascimento inválida. Use o formato YYYY-MM-DD.'}, 400

    hoje = datetime.today()
    idade_minima = hoje.replace(year=hoje.year - 14)

    if data_nascimento > idade_minima:
        return {'mensagem': 'É necessário ter pelo menos 14 anos para se registrar.'}, 400

    if len(senha) < 6 or len(senha) > 8:
        return {'mensagem': 'A senha deve ter entre 6 e 8 caracteres.'}, 400

    if Usuario.query.filter_by(email=email).first():
        return {'mensagem': 'Usuário já existe.'}, 400

    senha_criptografada = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    novo_usuario = Usuario(
        id=str(uuid.uuid4()),
        nome=nome,
        email=email,
        senha=senha_criptografada,
        data_nascimento=data_nascimento
    )

    db.session.add(novo_usuario)
    db.session.commit()
    return {'mensagem': 'Usuário registrado com sucesso!'}, 201


def login(data):
    from flask_jwt_extended import create_access_token

    email = data.get('email')
    senha = data.get('senha')

    if not email or not senha:
        return {'message': 'Email e senha obrigatórios!'}, 400

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or not bcrypt.checkpw(senha.encode('utf-8'), usuario.senha.encode('utf-8')):
        return {'message': 'Credenciais inválidas'}, 401

    # Gera token JWT usando flask_jwt_extended
    access_token = create_access_token(identity=str(usuario.id)) 
    return {'token': access_token, 'IdUsuario': usuario.id}, 200
