from flask.cli import FlaskGroup
from backend.app import create_app
from backend.app.db.config import db
from flask_migrate import Migrate

app = create_app()
cli = FlaskGroup(app)
migrate = Migrate(app, db)


@app.route("/")
def home():
    return "Flask está funcionando! 🚀"

if __name__ == "__main__":
    cli()
