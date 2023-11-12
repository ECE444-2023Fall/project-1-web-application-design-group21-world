import json
import os
import uuid
from datetime import datetime

from flask import flash, redirect, render_template, request, session, url_for
from flask_bootstrap import Bootstrap
from flask_login import (LoginManager, UserMixin, current_user, login_required, login_user,
                         logout_user)
from flask_migrate import Migrate
from flask_moment import Moment
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash

from app import create_app, db, login_manager
from app.main.event_form import EventForm
from app.main.forms import LoginForm, UserSignUpForm, userSignupInterestForm, UserDetailsChangeForm
from app.main.organizers.OrganizerSignUpForm import OrganizerSignupForm
from app.models import (Event, EventInterests, Interest, Organizer, OrganizerEvents,
                        OrganizerInterests, User, UserEvents, UserInterests)
from sqlalchemy.exc import IntegrityError


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
        print(f"Endpoint: {rule.endpoint}, Methods: {', '.join(rule.methods)}, Path: {rule}")

if __name__ == "__main__":
    print_routes(app)
    app.run(debug=True)
    
