from backend.app import create_app
from flask_mail import Message

# Criar a aplicação
app = create_app()

# Importar mail diretamente da aplicação
from backend.app import mail

# Função para enviar o e-mail de teste
def enviar_email():
    with app.app_context():  # Criando um contexto de aplicação Flask
        try:
            # Criando o e-mail de teste
            msg = Message(
                subject='Teste de E-mail',
                recipients=['karinyleandro0@gmail.com'],  # Altere para o seu e-mail
                body='Este é um teste de e-mail enviado com Flask-Mail.'
            )
            
            # Enviar o e-mail
            mail.send(msg)
            print("E-mail enviado com sucesso!")
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")

# Rodar o envio de e-mail ao executar o script
if __name__ == '__main__':
    enviar_email()
