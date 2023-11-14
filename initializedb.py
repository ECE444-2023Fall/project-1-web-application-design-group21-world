import random
import string

from app import db
from app.models import Event, Interest, User
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
        17: "Work & Career Development",
    }

    interests = []
    with app.app_context():
        for id, interest in interests_dict.items():
            interests.append(Interest(id=id, name=interest))
        db.session.add_all(interests)
        db.session.commit()


def create_events(num_events=10):
    """Generates num_events events with random values filled in each field. Use to populate Event database for testing

    Args:
        num_events (int, optional): Number of events to generate. Defaults to 10.
    """
    with app.app_context():
        for i in range(num_events):
            event = Event(
                event_name=generate_random_strings(10),
                organizer_id=random.choice(range(10)),
                description=generate_random_strings(500),
                date=generate_random_strings(10),
                time=generate_random_strings(10),
                location=generate_random_strings(10),
                google_map_link=generate_random_strings(10),
                fee=random.choice(range(20)),
                # has_rsvp=random.choice(["Yes", "No"]),
                external_registration_link=generate_random_strings(100),
            )
            # for interest in random.sample(Interest.query.all(), random.choice(range(3))):
            #     event.add_interest(interest)

            db.session.add(event)
        db.session.commit()


def create_users(num_users=10):
    """Generates num_events users with random values filled in each field. Use to populate User table for testing

    Args:
        num_events (int, optional): Number of events to generate. Defaults to 10.
    """
    with app.app_context():
        for i in range(num_users):
            user = User(
                name=generate_random_strings(10),
                email=f"{generate_random_strings(10)}@mail.utoronto.ca",
                password=generate_random_strings(15),
                faculty=generate_random_strings(10),
                major=generate_random_strings(5),
                campus=generate_random_strings(4),
                year_of_study=random.choice(range(1, 5)),
            )
            # for interest in random.sample(Interest.query.all(), random.choice(range(3))):
            #     user.add_interest(interest)
            for event in random.sample(
                Event.query.all(), random.choice(range(3))
            ):
                user.add_event(event)
            db.session.add(user)
        db.session.commit()


def generate_random_strings(length=10):
    letters = string.ascii_letters
    return "".join(random.choice(letters) for i in range(length))


if __name__ == "__main__":
    seed_interests()
    # create_events()
    # create_users()
