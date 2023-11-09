# create_db.py
from main import app, db

with app.app_context():
    db.drop_all()
    db.session.commit()
