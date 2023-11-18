from jsonschema import validate, ValidationError
from .exceptions import AppException

from functools import wraps
from flask import g


def validate_input_json(schema={}):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = kwargs.get("input")
            if data is None:
                return AppException(400, "can not decode json object")
            try:
                validate(data, schema)
            except ValidationError as e:
                if e.relative_path:
                    msg = f"Invalid value for '{e.relative_path[0]}'"
                else:
                    msg = e.message
                raise AppException(http_return_code=400, msg=msg)
            g.json_data = data
            return func(*args, **kwargs)

        return wrapper

    return decorator
