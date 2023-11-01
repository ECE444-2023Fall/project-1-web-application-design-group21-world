import os
import random

import pytest

from app import create_app, db
from app.models import User


@pytest.fixture
def client():
    app = create_app("testing")
    print("DATABASE URI PYTEST",app.config["SQLALCHEMY_DATABASE_URI"])
    
    with app.app_context():
        db.create_all()
        db.session.commit()
        
        yield app.test_client()
        db.drop_all
        
        


@pytest.fixture()
def new_user():
    num = random.randint(0,9999)
    
    user = User(username=f"utorid{num}", email=f"test.{num}@mail.utoronto.ca")
    
    print(user.username)
    print(user.email)
    return user



# @pytest.fixture()
# def app():
#     app = create_app("testing")
    

#     # other setup can go here

#     yield app

#     # clean up / reset resources here


# @pytest.fixture()
# def client(app):
#     return app.test_client()

# # @pytest.fixture(scope="module")
# # def client(app):
# #     app = create_app("testing")
# #     with app.test_client() as testing_client:
# #         db.create_all()
# #         with app.app_context():
# #             yield testing_client

# @pytest.fixture()
# def runner(app):
#     return app.test_cli_runner()



# @pytest.fixture()
# def init_database(client):
    
#     db.create_all()
#     default_user = User(username='default', email='email@utoronto.ca')
#     db.session.add(default_user)
#     db.session.commit()
#     yield

#     db.drop_all()


# # @pytest.fixture(scope="module")
# # def cli_test_client():
# #     app = create_app("testing")
# #     runner = app.test_cli_runner()

# #     yield runner

# # @pytest.fixture(scope='module')
# # def cli_test_client():
# #     # Set the Testing configuration prior to creating the Flask application
# #     # os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
# #     flask_app = create_app('testing')

# #     runner = flask_app.test_cli_runner()

# #     yield runner  # this is where the testing happens!
