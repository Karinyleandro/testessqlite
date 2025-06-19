import random
import string
import os
import traceback
import logging
import datetime
import bcrypt
from dotenv import load_dotenv
from flask import current_app
from flask_mail import Message
from email_validator import validate_email, EmailNotValidError
from backend.app.models.Usuario import Usuario
from backend.app.models.Endereco import Endereco
from backend.app.db.config import db

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dicionário para armazenar códigos de recuperação ativos {email: (codigo, data_expiracao)}
codigos_ativos = {}

# Função para gerar um código aleatório de 6 caracteres
def gerar_codigo(tamanho=6):
    caracteres = string.ascii_uppercase + string.digits
    return ''.join(random.choices(caracteres, k=tamanho))

# Função para enviar o e-mail de recuperação
def enviar_email_recuperacao(email, codigo):
    from backend.app import mail
    logger = logging.getLogger(__name__)

    print(f"[DEBUG] Enviando e-mail para: {email}")

    mensagem_texto = (
        f"Use o seguinte código para redefinir sua senha:\n\n{codigo}\n\n"
        "Este código expira em 1 hora. Não compartilhe com ninguém."
    )

    mensagem_html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #A662FF; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background: #FFFFFF; padding: 30px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <h2 style="color: #000000;">Recuperação de Senha</h2>
                <p style="color: #000000;">Olá,</p>
                <p style="color: #000000;">Você solicitou a redefinição da sua senha. Use o código abaixo:</p>
                <div style="background-color: #F0F0F0; color: #A662FF; padding: 15px; border-radius: 5px; font-size: 20px; text-align: center; font-weight: bold;">
                    {codigo}
                </div>
                <p style="color: #000000;">Este código expira em <strong>1 hora</strong>.</p>
                <p style="color: #FF0000;">Não compartilhe este código com ninguém.</p>
                <p style="color: #000000;">Se você não solicitou esta recuperação, ignore este e-mail.</p>
                <br>
                <p style="color: #000000;">Atenciosamente,<br>Equipe Lumyk</p>
            </div>
        </body>
    </html>
    """

    msg = Message(
        subject='Recuperação de Senha',
        sender=os.getenv('MAIL_DEFAULT_SENDER'),
        recipients=[email],
        body=mensagem_texto,
        html=mensagem_html
    )

    try:
        with current_app.app_context():
            mail.send(msg)
        return True
    except Exception as e:
        logger.error(f"Erro ao enviar e-mail: {e}")
        traceback.print_exc()
        return False

# Função para recuperar a senha (gera código e envia)
def recuperar_senha(data):
    email = data.get('email')
    try:
        validate_email(email)
    except EmailNotValidError as e:
        return {'mensagem': f'E-mail inválido: {str(e)}'}, 400

    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario:
        return {'mensagem': 'E-mail não encontrado.'}, 404

    codigo = gerar_codigo()
    expiracao = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    codigos_ativos[email] = (codigo, expiracao)

    if enviar_email_recuperacao(email, codigo):
        return {'mensagem': 'E-mail de recuperação enviado com sucesso.'}, 200
    else:
        return {'mensagem': 'Erro ao enviar o e-mail de recuperação.'}, 500

# Função para atualizar senha usando o código enviado por e-mail
def atualizar_senha(data):
    codigo_recebido = data.get('codigo')
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')

    if not codigo_recebido:
        return {'mensagem': 'Código é obrigatório.'}, 400

    # Verifica se o código é válido (mesmo se senha ainda não foi enviada)
    email_encontrado = None
    for email, (codigo, expiracao) in codigos_ativos.items():
        if codigo == codigo_recebido:
            email_encontrado = email
            break

    if not email_encontrado:
        return {'mensagem': 'Código inválido.'}, 401

    codigo_armazenado, expiracao = codigos_ativos[email_encontrado]
    if datetime.datetime.utcnow() > expiracao:
        del codigos_ativos[email_encontrado]
        return {'mensagem': 'O código expirou.'}, 401

    # Se senha não foi enviada ainda, só retorna sucesso
    if not new_password and not confirm_password:
        return {'mensagem': 'Código confirmado com sucesso.'}, 200

    # Agora validação da senha (caso esteja sendo enviada)
    if not new_password or not confirm_password:
        return {'mensagem': 'Nova senha e confirmação são obrigatórias.'}, 400

    if new_password != confirm_password:
        return {'mensagem': 'As senhas não conferem.'}, 400

    if len(new_password) < 6 or len(new_password) > 8:
        return {'mensagem': 'A senha deve ter entre 6 e 8 caracteres.'}, 400

    try:
        usuario = Usuario.query.filter_by(email=email_encontrado).first()
        if not usuario:
            return {'mensagem': 'Usuário não encontrado.'}, 404

        hoje = datetime.datetime.today()
        idade_minima = hoje.replace(year=hoje.year - 14)

        if not usuario.data_nascimento:
            return {'mensagem': 'Data de nascimento não cadastrada.'}, 400

        data_nasc = usuario.data_nascimento.date() if isinstance(usuario.data_nascimento, datetime.datetime) else usuario.data_nascimento

        if data_nasc > idade_minima.date():
            return {'mensagem': 'É necessário ter pelo menos 14 anos para atualizar a senha.'}, 400

        usuario.senha = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        db.session.commit()

        del codigos_ativos[email_encontrado]

        return {'mensagem': 'Senha atualizada com sucesso.'}, 200

    except Exception as e:
        logger.error(f'Erro inesperado ao atualizar senha: {str(e)}')
        return {'mensagem': f'Erro inesperado: {str(e)}'}, 500


# Função para atualizar o usuário
def atualizar_usuario(id, data):
    try:
        usuario = Usuario.query.get(id)
        if not usuario:
            return {'mensagem': 'Usuário não encontrado.'}, 404

        usuario.nome = data.get('nome', usuario.nome)
        usuario.email = data.get('email', usuario.email)

        data_nascimento_str = data.get('data_nascimento')
        if data_nascimento_str:
            try:
                usuario.data_nascimento = datetime.datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()
            except ValueError:
                return {'mensagem': 'Formato de data inválido. Use YYYY-MM-DD.'}, 400

        hoje = datetime.date.today()
        idade_minima = hoje.replace(year=hoje.year - 14)

        if isinstance(usuario.data_nascimento, datetime.datetime):
            usuario.data_nascimento = usuario.data_nascimento.date()

        if usuario.data_nascimento > idade_minima:
            return {'mensagem': 'É necessário ter pelo menos 14 anos para se registrar.'}, 400

        nova_senha = data.get('senha')
        if nova_senha:
            if len(nova_senha) < 6 or len(nova_senha) > 8:
                return {'mensagem': 'A senha deve ter entre 6 e 8 caracteres.'}, 400
            usuario.senha = bcrypt.hashpw(nova_senha.encode(), bcrypt.gensalt()).decode()

        db.session.commit()

        return {'mensagem': 'Usuário atualizado com sucesso.'}, 200

    except Exception as e:
        logger.error(f'Erro ao atualizar o usuário: {str(e)}')
        return {'mensagem': f'Erro ao atualizar o usuário: {str(e)}'}, 500

# Função para listar os usuários
def listar_usuarios():
    try:
        usuarios = Usuario.query.all()
        resultado = [
            {
                'id': usuario.id,
                'nome': usuario.nome,
                'email': usuario.email,
                'senha': usuario.senha
            }
            for usuario in usuarios
        ]
        return resultado, 200
    except Exception as e:
        logger.error(f'Ocorreu um erro ao listar os usuários: {str(e)}')
        return {'mensagem': f'Ocorreu um erro ao listar os usuários: {str(e)}'}, 500

# Função para buscar usuário por ID
def buscar_usuario_por_id(id):
    usuario = Usuario.query.get(id)
    if usuario:
        return {
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'data_nascimento': str(usuario.data_nascimento)
        }, 200
    else:
        return {'mensagem': 'Usuário não encontrado.'}, 404

# Função para deletar usuário
def deletar_usuario(id):
    try:
        usuario = Usuario.query.get(id)
        if not usuario:
            return {'mensagem': 'Usuário não encontrado.'}, 404

        # Buscar todos os endereços vinculados ao usuário
        enderecos = Endereco.query.filter_by(id_usuario=id).all()
        for endereco in enderecos:
            db.session.delete(endereco)

        # Agora deletar o usuário
        db.session.delete(usuario)
        db.session.commit()

        return {'mensagem': 'Usuário e endereços deletados com sucesso.'}, 200

    except Exception as e:
        logger.error(f'Erro ao deletar usuário: {str(e)}')
        return {'mensagem': f'Erro ao deletar usuário: {str(e)}'}, 500

