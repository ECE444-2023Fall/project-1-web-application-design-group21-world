# create_db.py
from app.models import User, Interest
from main import app, db


with app.app_context():
    db.drop_all()
    db.session.commit()
