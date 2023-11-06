# create_db.py
from app.models import User, Interest
from main import app, db

# List of interests to initialize
interests_data = [
    "Academic",
    "Arts",
    "Athletics",
    "Recreation",
    "Community Service",
    "Culture & Identities",
    "Environment & Sustainability",
    "Global Interest",
    "Hobby & Leisure",
    "Leadership",
    "Media",
    "Politics",
    "Social",
    "Social Justice and Advocacy",
    "Spirituality & Faith Communities",
    "Student Governments, Councils & Unions",
    "Work & Career Development"
]

with app.app_context():
    # create the database and the db table
    db.create_all()

    # commit the changes
    db.session.commit()
