from flask import Flask, request, jsonify, render_template
from ariadne import (
    graphql_sync,
    make_executable_schema,
    load_schema_from_path,
    snake_case_fallback_resolvers,
)
from werkzeug.exceptions import HTTPException

from .lib.ext import db, bcrypt, login_manager, migrate, cors
from .config import AppConfig

from .resolver import resolvers


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
    cors.init_app(app)

    type_def = load_schema_from_path("./src/graphql")
    schema = make_executable_schema(
        type_def,
        resolvers,
        snake_case_fallback_resolvers,
    )

    if AppConfig.IS_DEV:

        @app.route("/graphql", methods=["GET"])
        def gql_playground():
            """GraphQL playground for testing during development"""
            return render_template("graphql_playground.html")

    @app.route("/graphql", methods=["POST"])
    def gql():
        """Main GraphQL route"""
        data = request.get_json()
        success, result = graphql_sync(schema, data, context_value=request)
        status_code = 200 if success else 400
        return jsonify(result), status_code

    @app.errorhandler(HTTPException)
    def handle_exception(e: HTTPException):
        return {"error": e.description}, e.code

    return app
