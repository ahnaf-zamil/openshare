from flask import request
from flask_login import login_user

from ..exceptions import AppException
from ..model import Users
from ..lib.ext import db


class AuthService:
    @staticmethod
    def register_user():
        """Creates a new user"""
        user: Users = Users.query.filter(
            (Users.email == request.json["email"])
            | (Users.handle == request.json["handle"].lower())
        ).first()
        if user:
            raise AppException(http_return_code=409, msg="User already exists")

        new_user = Users(
            handle=request.json["handle"].lower(),
            username=request.json["username"],
            email=request.json["email"],
            password=request.json["password"],
        )
        db.session.add(new_user)
        db.session.commit()

        # Log in the user after first registration
        login_user(new_user)
        return new_user

    @staticmethod
    def login_user(email_or_handle: str):
        """Logs in user"""
        # Match by either email or handle
        user: Users = Users.query.filter(
            (Users.email == email_or_handle) | (Users.handle == email_or_handle)
        ).first()

        # Throw unauthorised if user doesn't exist, or if password is wrong
        if not user:
            raise AppException(http_return_code=401)
        if not user.check_password(request.json["password"]):
            raise AppException(http_return_code=401)

        # Log in the user if everything is alright
        login_user(user)
        return user
