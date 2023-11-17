from ...src.service.auth import AuthService
from ...src.exceptions import AppException
from sqlalchemy import inspect
from uuid import UUID

import pytest

svc = AuthService()


@pytest.mark.dependency()
def test_register_user_with_no_conflict(request_context):
    data = {
        "handle": "ahnaf.zamil",
        "email": "hi@ahnafzamil.com",
        "username": "Ahnaf",
        "password": "12345678",
    }

    with request_context(json=data) as ctx:
        user = svc.register_user()

    assert user.handle == data["handle"]
    assert user.username == data["username"]
    assert user.email == data["email"]

    assert user.check_password(data["password"])  # Checking PW hash
    assert UUID(user.id, version=4).hex == user.id  # Checking UUID generation
    assert not inspect(user).pending  # Checking if object has been committed

    assert ctx.session["_user_id"] == user.id  # Checking if session is being set


@pytest.mark.dependency(depends=["test_register_user_with_no_conflict"])
def test_register_user_with_conflict(request_context):
    """Scenario where entry with same email/handle exists

    Will run only if the test_register_user_with_no_conflict test runs, to make sure user data already exists

    Will throw 409 error if user already exists in DB
    """
    data = {
        "handle": "ahnaf.zamil",
        "email": "hi@ahnafzamil.com",
        "username": "Ahnaf",
        "password": "12345678",
    }

    with pytest.raises(AppException) as exc_info:
        with request_context(json=data):
            svc.register_user()

    assert exc_info.value.http_return_code == 409


@pytest.mark.dependency(depends=["test_register_user_with_no_conflict"])
def test_login_user_success(request_context):
    """Successful login test

    Will run only if the test_register_user_with_no_conflict test runs, to make sure user data already exists
    """
    # 1st case: User inputs his email in the 'email' field
    data = {
        "email": "hi@ahnafzamil.com",
        "password": "12345678",
    }

    with request_context(json=data) as ctx:
        user = svc.login_user(data["email"])

    assert ctx.session["_user_id"] == user.id
    assert user.email == data["email"]

    # 2nd case: User inputs his account handle in the 'email' field
    data["email"] = "ahnaf.zamil"

    with request_context(json=data) as ctx:
        user = svc.login_user(data["email"])

    assert ctx.session["_user_id"] == user.id
    assert user.handle == data["email"]


@pytest.mark.dependency(depends=["test_register_user_with_no_conflict"])
def test_login_user_failure(request_context):
    """Unsuccessful login test

    Will run only if the test_register_user_with_no_conflict test runs, to make sure user data already exists
    """
    # 1st case: User inputs inexistent user's email/handle
    data = {
        "email": "hi@wrongemail.com",
        "password": "12345678",
    }

    with pytest.raises(AppException) as exc_info:
        with request_context(json=data):
            svc.login_user(data["email"])
    assert exc_info.value.http_return_code == 401

    # 2nd case: User inputs wrong password
    data = {
        "email": "hi@ahnafzamil.com",
        "password": "wrongpassword",
    }

    with pytest.raises(AppException) as exc_info:
        with request_context(json=data):
            svc.login_user(data["email"])
    assert exc_info.value.http_return_code == 401
