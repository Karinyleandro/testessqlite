import jwt
import os
from datetime import datetime, timedelta
from flask_mail import Message
from . import mail  # Certifique-se de que o "mail" foi inicializado corretamente no __init__.py

# Função para gerar o token JWT
def generate_token(email):
    expiration = datetime.utcnow() + timedelta(hours=1)
    payload = {
        'email': email,
        'exp': expiration
    }
    secret_key = os.getenv('SECRET_KEY', 'default_secret')  # Pega a chave secreta do ambiente
    token = jwt.encode(payload, secret_key, algorithm='HS256')  # Geração do token
    return token

# Função para enviar o e-mail de recuperação com o token
def send_recovery_email(to_email, token):
    msg = Message(
        'Recuperação de Senha',
        sender='no-reply@seusite.com',  # Substitua com o seu e-mail de envio
        recipients=[to_email]
    )
    msg.body = (
        f"Use o seguinte código para recuperar sua senha:\n\n"
        f"{token}\n\n"
        f"Este código expira em 1 hora. Não compartilhe com ninguém."
    )

    try:
        mail.send(msg)  # Envia o e-mail
        return True
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {str(e)}")
        return False
