from flask import Flask
from . import users, posts


def register_controllers(app: Flask):
    app.register_blueprint(users.router)
    app.register_blueprint(posts.router)
    return print("Registered controllers")
