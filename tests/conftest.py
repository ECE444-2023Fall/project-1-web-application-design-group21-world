import os

import pytest

from app import create_app, db
from app.models import User


@pytest.fixture(scope="module")
def new_user():
    return User(username="utorid1234", email="test.user@mail.utoronto.ca")


@pytest.fixture(scope="module")
def test_client():
    app = create_app("testing")

    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture(scope="module")
def init_database(client):
    db.create_all()

    yield

    db.drop_all()


@pytest.fixture(scope="module")
def cli_test_client():
    app = create_app("testing")
    runner = app.test_cli_runner()

    yield runner
