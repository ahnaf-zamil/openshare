from jsonschema import validate, ValidationError
from .exceptions import AppException

from functools import wraps


def get_request_data(kwargs):
    """Returns data sent in the request in two formats"""
    # In case of query using input type, we need to access the input field of the body
    data = kwargs.get("input")

    if not data:
        # In case of query using parameters directly and no explicit input type, kwargs is the actual body
        data = kwargs
    return data


def validate_input_json(schema={}):
    """Custom validator for parameter/input data in GraphQL query, using Jsonschema"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = get_request_data(kwargs)
            try:
                validate(data, schema)
            except ValidationError as e:
                if e.relative_path:
                    msg = f"Invalid value for '{e.relative_path[0]}'"
                else:
                    msg = e.message
                raise AppException(http_return_code=400, msg=msg)
            return func(*args, **kwargs)

        return wrapper

    return decorator
