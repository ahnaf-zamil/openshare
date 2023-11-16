from uuid import uuid4
from flask_login import UserMixin
from ..lib.ext import db, bcrypt

import time


class Users(db.Model, UserMixin):
    """Users model"""

    __tablename__ = "users"

    id = db.Column(db.String(32), primary_key=True, default=lambda: uuid4().hex)
    handle = db.Column(db.String(30), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.Integer, default=lambda: int(time.time()), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

    @property
    def password(self):
        raise AttributeError("password: write-only field")

    @password.setter
    def password(self, pw: str):
        self.password_hash = bcrypt.generate_password_hash(pw).decode("utf-8")

    def check_password(self, pw: str):
        return bcrypt.check_password_hash(self.password_hash, pw)

    def __repr__(self):
        return f"User<id='{self.id}', handle='{self.handle}'>"

    def json(self):
        return {
            "id": self.id,
            "handle": self.handle,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at,
        }
