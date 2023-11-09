import os
import random

import pytest

from app import create_app, db
from app.models import User


@pytest.fixture
def client():
    app = create_app("testing")
    # print("DATABASE URI PYTEST",app.config["SQLALCHEMY_DATABASE_URI"])

    with app.app_context():
        db.create_all()
        db.session.commit()

        yield app.test_client()

        db.drop_all()


@pytest.fixture()
def new_user():
    num = random.randint(0, 9999)

    user = User(
        name=f"utorid{num}",
        email=f"test.{num}@mail.utoronto.ca",
        password=f"insecure{num}",
    )

    print(user.name)
    print(user.email)
    print(user.password)
    return user
