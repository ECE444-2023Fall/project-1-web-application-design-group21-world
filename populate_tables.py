import random
import string

from app import db
from app.models import Event, User
from main import app


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
                has_rsvp=random.choice(["Yes", "No"]),
                external_registration_link=generate_random_strings(100),
            )
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
                email=generate_random_strings(20),
                password=generate_random_strings(15),
                faculty=generate_random_strings(10),
                major=generate_random_strings(5),
                campus=generate_random_strings(4),
                year_of_study=generate_random_strings(10),
            )
            db.session.add(user)
        db.session.commit()


def generate_random_strings(length=10):
    letters = string.ascii_letters
    return "".join(random.choice(letters) for i in range(length))


if __name__ == "__main__":
    create_events()
    create_users()
