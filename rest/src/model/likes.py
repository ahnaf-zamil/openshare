from uuid import uuid4

from ..lib.ext import db

import time


class Likes(db.Model):
    """Model listing entity likes

    This single table will be used for both post and comment likes
    """

    __tablename__ = "likes"

    id = db.Column(db.String(32), primary_key=True, default=lambda: uuid4().hex)
    entity_type = db.Column(db.Integer, nullable=False)  # 0: Post, 1: Comment
    created_at = db.Column(db.Integer, default=lambda: int(time.time()), nullable=False)

    # ID of the entity (Post or Comment)
    entity_id = db.Column(db.String(32), nullable=False)

    # ID of the user
    user_id = db.Column(db.String(32), nullable=False)
