import os

from flask_migrate import Migrate

from app import create_app, db, login_manager
from app.models import (
    Event,
    EventInterests,
    Interest,
    Organizer,
    OrganizerEvents,
    OrganizerInterests,
    User,
    UserEvents,
    UserInterests,
)

app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, db)


# Register the user loader function
@login_manager.user_loader
def load_user(user_id):
    # Assuming User and Organizer are separate models
    # Check if the user ID corresponds to a User
    user = User.query.get(user_id)
    organizer = Organizer.query.get(user_id)
    if user:
        return user
    elif organizer:
        return organizer
    return None


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        User=User,
        Interest=Interest,
        Organizer=Organizer,
        Event=Event,
        UserEvents=UserEvents,
        OrganizerEvents=OrganizerEvents,
        UserInterests=UserInterests,
        OrganizerInterests=OrganizerInterests,
        EventInterests=EventInterests,
    )


def print_routes(app):
    """Print all registered routes in a Flask app."""
    for rule in app.url_map.iter_rules():
        print(
            f"Endpoint: {rule.endpoint}, Methods: {', '.join(rule.methods)}, Path: {rule}"
        )


if __name__ == "__main__":
    app.run()
