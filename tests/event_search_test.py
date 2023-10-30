# import os
# import pytest
# import sqlite3
# from pathlib import Path
# import json

# from app import app, db
# from app.models import User
# from app.models import * 

# TEST_DB = "test.db"

# DATABASE = "data.sqlite"
# SQLALCHEMY_DATABASE_URI = f"sqlite:///{Path(basedir).joinpath(DATABASE)}"
# SQLALCHEMY_TRACK_MODIFICATIONS = False

# @pytest.fixture
# def client():
#     BASE_DIR = Path(__file__).resolve().parent.parent
#     app.config["TESTING"] = True
#     app.config["DATABASE"] = BASE_DIR.joinpath(TEST_DB)
#     app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{BASE_DIR.joinpath(TEST_DB)}"

#     with app.app_context():
#         db.create_all()  # setup
#         yield app.test_client()  # tests run here
#         db.drop_all()  # teardown

# def test_event_search(client):
#     event_id = {
#         'event_id':1
#     }
#     response = client.get('events/search',json=Event)

#     with app.app_context():
#         event = events.query.get(event_id=1).first()
#         assert event is not None 
#         assert event_id == 1
        
