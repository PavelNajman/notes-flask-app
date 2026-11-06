from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import config

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()


def create_app(config_name: str = "default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    api = Api(app)

    from .notes.api import blp as NotesBlueprint

    api.register_blueprint(NotesBlueprint)

    return app
