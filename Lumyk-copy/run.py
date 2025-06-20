from backend.app import create_app
import os

app = create_app()

port = int(os.environ.get("PORT", 5000))  # Pega a porta do Render, senão 5000

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)

'''
    Para rodar o código e visualizar a documentação da API:
        python run.py
        http://127.0.0.1:5000/docs

'''