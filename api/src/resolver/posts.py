from ariadne import MutationType, QueryType
from graphql import GraphQLResolveInfo
from flask_login import login_required
from ..service.post import PostService
from ..util import validate_input_json, get_request_data
from ..lib.graphql import ResolverGroup

group = ResolverGroup(MutationType, QueryType)


post_get_like_delete_input = {
    "type": "object",
    "properties": {
        "post_id": {
            "type": "string",
            "minLength": 32,
            "maxLength": 32,  # UUID length without hyphens
        },
    },
    "required": ["post_id"],
}


@group.field("getPost", QueryType)
@validate_input_json(post_get_like_delete_input)
def get_post(_, info: GraphQLResolveInfo, **kwargs):
    data = get_request_data(kwargs)
    return PostService.get_post(data["post_id"]).json()


@group.field("createPost", MutationType)
@login_required
@validate_input_json(
    {
        "type": "object",
        "properties": {
            "caption": {"type": "string", "minLength": 1, "maxLength": 2000},
        },
        "required": ["caption"],
    }
)
def create_post(_, info: GraphQLResolveInfo, **kwargs):
    data = get_request_data(kwargs)
    post_data = PostService.create_post(data["caption"])
    return post_data.json()


@group.field("updatePost", MutationType)
@login_required
@validate_input_json(
    {
        "type": "object",
        "properties": {
            "caption": {"type": "string", "minLength": 1, "maxLength": 2000},
            "post_id": {
                "type": "string",
                "format": "uuid",
                "minLength": 32,
                "maxLength": 32,
            },
        },
        "required": ["caption", "post_id"],
    }
)
def update_post(_, info: GraphQLResolveInfo, **kwargs):
    data = get_request_data(kwargs)
    post_data = PostService.update_post(data["post_id"], data["caption"])
    return post_data.json()


@group.field("deletePost", MutationType)
@login_required
@validate_input_json(post_get_like_delete_input)
def delete_post(_, info: GraphQLResolveInfo, **kwargs):
    data = get_request_data(kwargs)
    PostService.delete_post(data["post_id"])
    return True


@group.field("likePost", MutationType)
@login_required
@validate_input_json(post_get_like_delete_input)
def like_post(_, info: GraphQLResolveInfo, **kwargs):
    data = get_request_data(kwargs)
    PostService.like_post(data["post_id"])
    return True
