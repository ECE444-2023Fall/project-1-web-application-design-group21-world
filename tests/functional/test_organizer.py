from flask import url_for

from app.models import Organizer


def test_organizer_insert(client):
    """Ensure that organizers can be added to Organizer Table"""
    test_organizer = dict(
        organizer_name="test organizer 01",
        organizer_email="testorganizer01@gmail.com",
    )

    response = client.post(
        "/organizer/create", json=test_organizer, follow_redirects=True
    )
    assert response.status_code == 200
    with client:
        organizer = Organizer.query.filter_by(
            organizer_name=test_organizer["organizer_name"]
        ).first()
        assert organizer is not None
        assert organizer.organizer_email == test_organizer["organizer_email"]
        assert organizer.organizer_name == test_organizer["organizer_name"]


def test_organizer_insert_multiple(client):
    """Ensure that organizers can be added to Organizer Table"""
    test_organizer = dict(
        organizer_name="test organizer 02",
        organizer_email="testorganizer02@gmail.com",
    )

    response = client.post(
        "/organizer/create", json=test_organizer, follow_redirects=True
    )
    assert response.status_code == 200
    with client:
        organizer = Organizer.query.filter_by(
            organizer_name=test_organizer["organizer_name"]
        ).first()
        assert organizer is not None
        assert organizer.organizer_email == test_organizer["organizer_email"]
        assert organizer.organizer_name == test_organizer["organizer_name"]
