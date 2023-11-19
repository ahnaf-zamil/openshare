from ...src.service.post import PostService
from ..util import _login_user
from flask_login import current_user
from ...src.exceptions import AppException
from ...src.model.likes import Likes
from sqlalchemy import inspect
from uuid import UUID

import pytest

svc = PostService()

# Global variable to store created post ID from post creation test, this will be later used to query
created_post = ""


@pytest.mark.dependency()
# All other post related tests will run after this one finishes, since we need the ID of the created post
def test_create_post(request_context):
    global created_post
    data = {
        "caption": "This is a post",
    }

    with request_context(json=data):
        # Logging in user to use the session
        _login_user(request_context)
        new_post = svc.create_post(caption=data["caption"])

        assert new_post.caption == data["caption"]
        assert (
            UUID(new_post.id, version=4).hex == new_post.id
        )  # Checking UUID generation
        assert not inspect(new_post).pending  # Checking if object has been committed

        created_post = new_post.json()  # Setting it to use later on


@pytest.mark.dependency(depends=["test_create_post"])
def test_get_post_success(request_context):
    with request_context():
        post = svc.get_post(created_post["id"])

        assert post.id == created_post["id"]
        assert post.caption == created_post["caption"]
        assert post.created_at == created_post["created_at"]


def test_get_post_failure(request_context):
    with pytest.raises(AppException) as exc_info:
        with request_context():
            svc.get_post("inexistent post id")
        assert exc_info.value.http_return_code == 404


@pytest.mark.dependency(depends=["test_create_post"])
def test_update_post_success(request_context):
    new_caption = "Edited caption"
    with request_context():
        # Logging in user to use the session
        _login_user(request_context)
        post = svc.update_post(created_post["id"], new_caption)

        assert post.id == created_post["id"]
        assert post.caption == new_caption
        assert post.created_at == created_post["created_at"]


def test_update_post_failure(request_context):
    new_caption = "Edited caption"
    with pytest.raises(AppException) as exc_info:
        with request_context():
            # Logging in user to use the session
            _login_user(request_context)
            svc.update_post("inexistent post id", new_caption)
        assert exc_info.value.http_return_code == 404


@pytest.mark.dependency(depends=["test_create_post"])
def test_like_post(request_context):
    with request_context():
        # Logging in user to use the session
        _login_user(request_context)
        svc.like_post(created_post["id"])

        new_like = Likes.query.filter_by(
            entity_type=0, entity_id=created_post["id"], user_id=current_user.id
        ).first()
        assert new_like


@pytest.mark.dependency(depends=["test_create_post", "test_like_post"])
def test_unlike_post(request_context):
    """Checking to see if liking a post again after liking it once removes it from DB or not i.e unliking"""
    with request_context():
        # Logging in user to use the session
        _login_user(request_context)
        svc.like_post(created_post["id"])

        like = Likes.query.filter_by(
            entity_type=0, entity_id=created_post["id"], user_id=current_user.id
        ).first()
        assert not like


@pytest.mark.dependency(depends=["test_create_post"])
def test_delete_post(request_context):
    with request_context():
        # Logging in user to use the session
        _login_user(request_context)
        assert not svc.delete_post(created_post["id"])

        with pytest.raises(AppException) as exc_info:
            svc.get_post(created_post["id"])
            assert exc_info.value.http_return_code == 404
