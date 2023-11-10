# create_db.py
from app.models import Interest, User
from main import app, db

with app.app_context():
    db.drop_all()
    db.session.commit()
