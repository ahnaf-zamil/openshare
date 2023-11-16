from flask import Flask

from .controller import register_controllers
from .lib.ext import db, bcrypt, login_manager, migrate
from .config import AppConfig


def create_app(is_testing=False):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///.\\test.db" if is_testing else AppConfig.DATABASE_URI
    )
    app.config["SECRET_KEY"] = AppConfig.SECRET_KEY
    app.config["SESSION_COOKIE_SAMESITE"] = "None"
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_HTTPONLY"] = True

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    register_controllers(app)
    return app
