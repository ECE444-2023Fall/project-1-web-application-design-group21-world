# import json
# from pathlib import Path

# import pytest

# from app.models import User
# from app import create_app, db


# @pytest.fixture
# def client():

#     app = create_app('testing')

#     with app.app_context():
#         db.create_all()  # setup
#         yield app.test_client()  # tests run here
#         db.drop_all()  # teardown


# def test_user_insert(client):
#     """Ensure that users can be added to User table"""
#     test_user = dict(username="testname", email="testemail@mail.utoronto.ca")
#     with app.app_context():
#         users = User.query.all()
#         assert len(users) == 0

#     response = client.post(
#         "/users/create",
#         data=test_user,
#     )
#     assert response.status_code == 200

#     with app.app_context():
#         users = User.query.all()
#         assert len(users) == 1
#         assert users[0].id == 1
#         assert users[0].username == test_user["username"]
#         assert users[0].email == test_user["email"]
