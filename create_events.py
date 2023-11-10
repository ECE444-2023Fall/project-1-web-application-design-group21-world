import random
import string

from app import db
from app.models import Event
from main import app


def create_events(num_events=10):
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


def generate_random_strings(length=10):
    letters = string.ascii_letters
    return "".join(random.choice(letters) for i in range(length))


if __name__ == "__main__":
    create_events()
