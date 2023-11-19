from uuid import uuid4

from ..lib.ext import db

import time


class Posts(db.Model):
    """Posts model"""

    __tablename__ = "posts"

    id = db.Column(db.String(32), primary_key=True, default=lambda: uuid4().hex)
    caption = db.Column(db.String(2000), nullable=False)
    created_at = db.Column(db.Integer, default=lambda: int(time.time()), nullable=False)

    # ID of the user who created the post
    user_id = db.Column(db.String(32), nullable=False)

    def json(self):
        return {
            "id": self.id,
            "caption": self.caption,
            "created_at": self.created_at,
            "user_id": self.user_id,
        }


class PostMedia(db.Model):
    """Model containing information about post media (images and videos)"""

    __tablename__ = "post_media"

    id = db.Column(db.String(32), primary_key=True, default=lambda: uuid4().hex)
    filename = db.Column(db.Text, nullable=False)
    index = db.Column(db.Integer, nullable=False)

    # ID of the post
    post_id = db.Column(db.String(32), nullable=False)
