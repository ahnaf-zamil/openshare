from functools import wraps
from .exceptions import AppException


def handle_app_exception(f):
    """A decorator that handles custom app exceptions
    Custom error messages are returned to clients
    """

    @wraps(f)
    def dec(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except AppException as e:
            return {"error": e.message} if e.message else "", e.http_return_code

    return dec
