from flask_login import login_user

from ..exceptions import AppException
from ..model import Users
from ..lib.ext import db, login_manager


@login_manager.user_loader
def load_user(user_id: str):
    return Users.query.filter(Users.id == user_id).first()


class AuthService:
    @staticmethod
    def register_user(username: str, handle: str, email: str, password: str):
        """Creates a new user"""
        user: Users = Users.query.filter(
            (Users.email == username) | (Users.handle == handle.lower())
        ).first()
        if user:
            raise AppException(http_return_code=409, msg="User already exists")

        new_user = Users(
            handle=handle.lower(),
            username=username,
            email=email,
            password=password,
        )
        db.session.add(new_user)
        db.session.commit()

        # Log in the user after first registration
        login_user(new_user)
        return new_user

    @staticmethod
    def login_user(email: str, password: str):
        """Logs in user"""
        # Match by either email or handle
        user: Users = Users.query.filter(
            (Users.email == email) | (Users.handle == email)
        ).first()

        # Throw unauthorised if user doesn't exist, or if password is wrong
        if not user:
            raise AppException(http_return_code=401)
        if not user.check_password(password):
            raise AppException(http_return_code=401)

        # Log in the user if everything is alright
        login_user(user)
        return user
