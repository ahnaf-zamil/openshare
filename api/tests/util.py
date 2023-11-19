from ..src.service.auth import AuthService


def _login_user(request_context):
    data = {
        "email": "hi@ahnafzamil.com",
        "password": "12345678",
    }
    AuthService().login_user(data["email"], data["password"])
