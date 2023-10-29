import json
from pathlib import Path

import pytest

from app import app, db
from app.models import *

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

def test_create_organizer(client):
    # Define user data for testing
    organizer_data = {
        'organizer_name':'test_organizer_01',
        'organizer_email' : 'test_organizer_01@gmail.com',
        'description' : 'test_organizer_desription',
        'contact_email' : 'test_organizer_contact_email',
    }

    # Send a POST request to add the user
    response = client.post('/organizer/create', json=organizer_data)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Verify that the user has been added to the database
    with app.app_context():
        organizer = Organizer.query.filter_by(organizer_name='test_organizer_01').first()
        assert organizer is not None
        assert organizer.organizer_email == 'test_organizer_01@gmail.com'

def test_get_organizer(client):
    pass
    #Add get request which checks organizer