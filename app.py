""" app.py """
from flask import Flask
from flask_migrate import Migrate

from api import api_bp
from config import Config
from models import db, bcrypt
from jwt_token import jwt


app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(api_bp)

db.init_app(app)
migrate = Migrate(app, db)

bcrypt.init_app(app)

jwt.init_app(app)


@app.route("/")
def hello_world():
    """ hello_world() """
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    app.run(host=app.config['RUN_HOST'], port=app.config['RUN_PORT'])
