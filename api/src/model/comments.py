from uuid import uuid4

from ..lib.ext import db

import time


class Comments(db.Model):
    """Model containing information about post comments"""

    __tablename__ = "comments"

    id = db.Column(db.String(32), primary_key=True, default=lambda: uuid4().hex)
    content = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.Integer, default=lambda: int(time.time()), nullable=False)

    # If it's a one-level reply, this is the ID of the parent comment this reply belongs to
    # Nullable since top level comments cannot have parents
    parent_id = db.Column(db.String(32))

    # ID of the post
    post_id = db.Column(db.String(32), nullable=False)

    # ID of the user
    user_id = db.Column(db.String(32), nullable=False)
