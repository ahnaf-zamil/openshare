from flask import Blueprint, request
from flask_login import login_required
from flask_validate_json import validate_json

from ..wrappers import handle_app_exception
from ..service.post import PostService
from ..util import bad_request_resp

router = Blueprint("posts", __name__, url_prefix="/posts")

post_create_schema = {
    "type": "object",
    "properties": {
        "caption": {"type": "string", "minLength": 1, "maxLength": 2000},
    },
    "required": ["caption"],
}


@router.post("/create")
@handle_app_exception
@login_required
@validate_json(post_create_schema, resp_func=bad_request_resp)
def create_post():
    post_data = PostService.create_post(request.json["caption"])
    return post_data.json(), 201


@router.patch("/update/<post_id>")
@handle_app_exception
@login_required
@validate_json(post_create_schema, resp_func=bad_request_resp)
def update_post(post_id: str):
    post_data = PostService.update_post(post_id, request.json["caption"])
    return post_data.json(), 200


@router.delete("/delete/<post_id>")
@handle_app_exception
@login_required
def delete_post(post_id: str):
    PostService.delete_post(post_id)
    return "", 200


@router.post("/like/<post_id>")
@handle_app_exception
@login_required
def like_post(post_id: str):
    PostService.like_post(post_id)
    return "", 200
