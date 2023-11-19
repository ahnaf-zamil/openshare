from flask_login import current_user
from typing import Optional
from ..exceptions import AppException
from ..model import Posts, Likes
from ..lib.ext import db


class PostService:
    @staticmethod
    def get_post(post_id: str) -> Optional[Posts]:
        """Fetches post from DB"""
        post = Posts.query.filter_by(id=post_id).first()
        if not post:
            raise AppException(http_return_code=404, msg="Post not found")
        return post

    @staticmethod
    def create_post(caption: str) -> Posts:
        """Creates a new post"""
        new_post = Posts(caption=caption, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()

        return new_post

    @staticmethod
    def update_post(post_id: str, caption: str) -> Posts:
        """Updates an existing post"""
        post = Posts.query.filter_by(id=post_id).first()

        if not post:
            raise AppException(404, "Post not found")

        post.caption = caption
        db.session.commit()

        return post

    @staticmethod
    def delete_post(post_id: str) -> None:
        """Deletes a post"""
        post: Optional[Posts] = Posts.query.filter_by(id=post_id).first()

        if not post:
            raise AppException(404, "Post not found")

        if post.user_id != current_user.id:
            raise AppException(403, "You are not the post owner")

        db.session.delete(post)
        return db.session.commit()

    @staticmethod
    def like_post(post_id: str) -> None:
        """Likes a post by a user"""
        post = Posts.query.filter_by(id=post_id).first()

        if not post:
            raise AppException(404, "Post not found")

        # Checking for existing post like
        existing_like = Likes.query.filter_by(
            entity_type=0, entity_id=post_id, user_id=current_user.id
        ).first()
        if existing_like:
            # If user has liked this post already, delete the like
            db.session.delete(existing_like)
        else:
            # If not, create a like for the post
            new_like = Likes(entity_type=0, entity_id=post_id, user_id=current_user.id)
            db.session.add(new_like)
        return db.session.commit()
