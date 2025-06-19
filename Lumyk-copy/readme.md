 📚 Lumyk Backend

Este é o backend de um sistema de gestão de livros, autores, gêneros e pedidos feito com Flask, utilizando Flask-RESTx para documentação automática e JWT para autenticação. A aplicação utiliza SQLAlchemy como ORM e Flask-Migrate para controle de migrations.

 📥 Como Clonar o Repositório

Para clonar este projeto em sua máquina:
  
  ```bash
  git clone https://github.com/Karinyleandro/Lumyk---backend.git
  ```
Depois, acesse a pasta do projeto:

  ```bash
  cd Lumyk---backend
  ```
---

📦 Instalação

Clone o repositório (conforme instrução acima).
Navegue até a pasta do projeto.
Instale as dependências:

```bash
pip install -r C:\Users\karin\Lumyk---backend\requirements.txt
```

Para rodar as migrations e criar o banco de dados:
```bash
flask --app manage.py db upgrade --directory backend/app/migrations
```

Executar Seeders (Inserir Dados Iniciais)
Para popular as tabelas com os dados principais:
```bash
PYTHONPATH=backend python -m backend.app.db.seeders.seeder
```

Se tudo ocorrer bem, você verá:

  Autores inseridos com sucesso!
  
  Gêneros inseridos com sucesso!
  
  Livros inseridos com sucesso!


 🚀 Rodando a Aplicação
Para iniciar a aplicação e acessar a documentação da API:
```bash
python run.py
```
Acesse no navegador:
```bash
http://127.0.0.1:5000/docs
```
---------------------------------------------------------------------------------------------------------------
 OBS: CASO DÊ ALGUM ERRO POR FALTA DE ALGUMA INSTALAÇÃO, RODE:
```bash
pip install Flask==3.1.0 Flask-RESTX==1.1.0 python-dotenv==1.0.0
```
ou, se preciso continuar, modifique a versão para:
```` bash
pip install flask-restx==1.3.0
````
ESSE PACOTE DE CIMA RESOLVE ESSE ERRO DE BAIXO:

```bash
Error: While importing 'manage', an ImportError was raised:

Traceback (most recent call last):
  File "C:\Users\laura\AppData\Local\Programs\Python\Python311\Lib\site-packages\flask\cli.py", line 218, in locate_app
    _import_(module_name)
  File "C:\Users\laura\Desktop\Lumyk\Lumyk---backend\manage.py", line 2, in <module>
    from backend.app import create_app
  File "C:\Users\laura\Desktop\Lumyk\Lumyk---backend\backend\app\_init_.py", line 3, in <module>
    from flask_restx import Api
  File "C:\Users\laura\AppData\Local\Programs\Python\Python311\Lib\site-packages\flask_restx\_init_.py", line 2, in <module>
    from .api import Api  # noqa
    ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\laura\AppData\Local\Programs\Python\Python311\Lib\site-packages\flask_restx\api.py", line 35, in <module>
    from werkzeug import _version_ as werkzeug_version
ImportError: cannot import name '_version' from 'werkzeug' (C:\Users\laura\AppData\Local\Programs\Python\Python311\Lib\site-packages\werkzeug\init_.py)
```
---------------------------------------------------------------------------------------------------------------
E SE TIVER OUTRO ERRO RELACIONADO A NAO TER ACHADO UM MODULO BCRYPT, INSTALE:
```bash
pip install bcrypt
```

```bash
Error: While importing 'manage', an ImportError was raised:

Traceback (most recent call last):
  File "C:\Users\laura\AppData\Local\Programs\Python\Python311\Lib\site-packages\flask\cli.py", line 245, in locate_app
    _import_(module_name)
  File "C:\Users\laura\Desktop\Lumyk\Lumyk---backend\manage.py", line 2, in <module>
    from backend.app import create_app
  File "C:\Users\laura\Desktop\Lumyk\Lumyk---backend\backend\app\_init_.py", line 6, in <module>
    from backend.app.routes.usuario_routes import api as usuario
  File "C:\Users\laura\Desktop\Lumyk\Lumyk---backend\backend\app\routes\usuario_routes.py", line 3, in <module>
    from backend.app.controllers import UsuarioController
  File "C:\Users\laura\Desktop\Lumyk\Lumyk---backend\backend\app\controllers\_init_.py", line 1, in <module>
    from .authUsuario import *
  File "C:\Users\laura\Desktop\Lumyk\Lumyk---backend\backend\app\controllers\authUsuario.py", line 1, in <module>
    import bcrypt
ModuleNotFoundError: No module named 'bcrypt'
```

---
OBSERVAÇÃO: configure a váriavel de ambiente no arquivo .env que se encontra no diretório principal do backend.

   - Exemplo de chave secreta usada para geração e validação de tokens JWT:
 ```
   JWT_SECRET=sua_chave_super_secreta_aqui
```

---
Configuração do arquivo .env:
Além da senha configurada como recomendado acima, será preciso que você configure os arquivos para smtp:
Se precisar que eu informe a senha de app do email que eu usei é só entrar em contato


Configure no .env também a expiração do token:

```
#tempo de expirar
JWT_ACCESS_TOKEN_EXPIRES=False
```

```
#smtp
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=lumykbooks@gmail.com
MAIL_PASSWORD=#senhadoapp
MAIL_DEFAULT_SENDER=lumykbooks@gmail.com
```

---
PARA RODAR A RECUPERAÇÃO DE SENHA, É PRECISO INSTALAR:

```bash
pip install Flask-Mail
pip install email-validator
```
