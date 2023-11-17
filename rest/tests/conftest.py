from dotenv import load_dotenv

load_dotenv(".env.testing")

from ..src.app import create_app
from ..src.lib.ext import db as _db

from flask_migrate import upgrade

import pytest

_app = create_app(is_testing=True)


@pytest.fixture(scope="session")
def app():
    """Returns an app object which uses in-memory database"""
    return _app


@pytest.fixture()
def db():
    """Returns an SQLAlchemy db object"""
    return _db


@pytest.fixture()
def request_context(app):
    return app.test_request_context


def pytest_sessionstart(session):
    """Running DB migration upon test start"""
    with _app.app_context():
        upgrade()


def pytest_sessionfinish(session):
    """Clearing up database"""
    with _app.app_context():
        _db.reflect()
        _db.drop_all()
