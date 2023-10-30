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

#Contributed by Modhurima Roy Kenopy
def test_create_event(client):
    # Define event data for testing
    event_data = {
        'event_name': 'Test Event',
        'description': 'This is a test event.'
    }

    # Send a POST request to add the event
    response = client.post('/event/create', json=event_data)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Verify that the user has been added to the database
    with app.app_context():
        event = Event.query.filter_by(event_name='Test Event').first()
        assert event is not None
        assert event.description == 'This is a test event.'

#Contributed by Nisha Malik
def test_event_search(client):
    event_id = {
        'event_id':1
    }
    response = client.get('events/search',json=Event)

    with app.app_context():
        event = events.query.get(event_id=1).first()
        assert event is not None 
        assert event_id == 1
        
#Contributed by Ria Malhotra
def test_database(client):
    """Test whether database exists"""
    assert Path("organizer.db").is_file()

def test_get_organizer(client):
    """Test whether search gets correct organizer"""
    organizer_data = {
        'organizer_name':'test_organizer_02',
        'organizer_email' : 'test_organizer_02@gmail.com',
        'description' : 'test_organizer_desription',
        'contact_email' : 'test_organizer_contact_email',
    }

    response = client.post('/organizer/create', json=organizer_data)
    get_response = client.get('/organizer/test_organizer_02')

    assert response.status_code == 200

    with app.app_context():
        organizer = get_response.json
        assert organizer['organizer_name'] == 'test_organizer_02'
        assert organizer['organizer_email'] == 'test_organizer_02@gmail.com'
        assert organizer['description'] == 'test_organizer_description'
        assert organizer['contact_email'] == 'test_organizer_contact_email'
