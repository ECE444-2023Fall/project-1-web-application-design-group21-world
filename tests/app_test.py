import json
from pathlib import Path

import pytest

from app import app, db
from app.models import User

TEST_DB = "test.db"

@pytest.fixture
def client():
    BASE_DIR = Path(__file__).resolve().parent.parent
    app.config["TESTING"] = True
    app.config["DATABASE"] = BASE_DIR.joinpath(TEST_DB)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{BASE_DIR.joinpath(TEST_DB)}"

    with app.app_context():
        db.create_all()  # setup
        yield app.test_client()  # tests run here
        db.drop_all()  # teardown

#Contributed by Rishabh Saini
def test_add_user(client):
    # Define user data for testing
    user_data = {
        'username': 'testuser',
        'email': 'testuser@example.com'
    }

    # Send a POST request to add the user
    response = client.post('/users/create', json=user_data)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Verify that the user has been added to the database
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        assert user is not None
        assert user.email == 'testuser@example.com'
