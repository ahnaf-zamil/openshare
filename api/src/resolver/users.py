from ariadne import MutationType, QueryType
from graphql import GraphQLResolveInfo
from flask_login import login_required, current_user
from ..service.auth import AuthService
from ..util import validate_input_json
from ..lib.graphql import ResolverGroup

group = ResolverGroup(MutationType, QueryType)


@group.field("getCurrentUser", QueryType)
@login_required
def get_current_user(_, info: GraphQLResolveInfo):
    return current_user.json()


@group.field("registerUser", MutationType)
@validate_input_json(
    {
        "type": "object",
        "properties": {
            "handle": {
                "type": "string",
                "minLength": 3,
                "maxLength": 30,
                "pattern": "^[a-z0-9._]+$",
            },
            "username": {"type": "string", "minLength": 3, "maxLength": 50},
            "email": {
                "type": "string",
                "minLength": 6,
                "maxLength": 255,
                "format": "email",
                "pattern": r"^(\S[A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+$",
            },
            "password": {"type": "string", "minLength": 8, "maxLength": 1000},
        },
        "required": ["email", "password"],
    }
)
def register_user(_, info: GraphQLResolveInfo, **kwargs):
    data = kwargs["input"]
    new_user = AuthService.register_user(**data)
    return new_user.json()


@group.field("loginUser", MutationType)
@validate_input_json(
    {
        "type": "object",
        "properties": {
            "email": {"type": "string", "minLength": 6, "maxLength": 255},
            "password": {"type": "string", "minLength": 8, "maxLength": 1000},
        },
        "required": ["email", "password"],
    }
)
def login_user(_, info: GraphQLResolveInfo, **kwargs):
    data = kwargs["input"]
    existing_user = AuthService.login_user(**data)
    return existing_user.json()
