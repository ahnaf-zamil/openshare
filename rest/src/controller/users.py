from flask import Blueprint, request
from flask_login import current_user, login_required
from flask_validate_json import validate_json

from ..wrappers import handle_app_exception
from ..service.auth import AuthService
from ..util import bad_request_resp
from ..model import Users
from ..lib.ext import login_manager


@login_manager.user_loader
def load_user(user_id: str):
    return Users.query.filter(Users.id == user_id).first()


router = Blueprint("users", __name__, url_prefix="/users")

register_schema = {
    "type": "object",
    "properties": {
        "handle": {
            "type": "string",
            "minLength": 3,
            "maxLength": 30,
            "pattern": "^[a-z0-9._]+$",
        },
        "username": {"type": "string", "minLength": 3, "maxLength": 50},
        "email": {
            "type": "string",
            "minLength": 6,
            "maxLength": 255,
            "format": "email",
            "pattern": r"^(\S[A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+$",
        },
        "password": {"type": "string", "minLength": 8, "maxLength": 1000},
    },
    "required": ["handle", "username", "email", "password"],
}


@router.post("/register")
@handle_app_exception
@validate_json(register_schema, resp_func=bad_request_resp)
def register_user():
    AuthService.register_user()
    return "", 200


login_schema = {
    "type": "object",
    "properties": {
        "email": {"type": "string", "minLength": 6, "maxLength": 255},
        "password": {"type": "string", "minLength": 8, "maxLength": 1000},
    },
    "required": ["email", "password"],
}


@router.post("/login")
@handle_app_exception
@validate_json(login_schema, resp_func=bad_request_resp)
def auth_user():
    email_or_handle = request.json["email"].lower()
    AuthService.login_user(email_or_handle)
    return "", 200


@router.get("/me")
@login_required
def get_current_user():
    return current_user.json()
