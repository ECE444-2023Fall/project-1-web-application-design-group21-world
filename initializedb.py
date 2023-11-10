from app import db
from app.models import Interest
from main import app

def seed_interests():
    interests_dict = {
        1: "Academics",
        2: "Arts",
        3: "Athletics",
        4: "Recreation",
        5: "Community Service",
        6: "Culture & Identities",
        7: "Environment & Sustainability",
        8: "Global Interest",
        9: "Hobby & Leisure",
        10: "Leadership",
        11: "Media",
        12: "Politics",
        13: "Social",
        14: "Social Justices and Advocacy",
        15: "Spirituality & Faith Communities",
        16: "Student Governments, Councils & Unions",
        17: "Work & Career Development"
    }

    interests = []
    with app.app_context():
        for id, interest in interests_dict.items():
            interests.append(Interest(id=id, name=interest))
        db.session.add_all(interests)
        db.session.commit()

if __name__ == '__main__':
    seed_interests()