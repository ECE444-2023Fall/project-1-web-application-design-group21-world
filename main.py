import json
import os
from datetime import datetime

from flask import flash, redirect, render_template, request, session, url_for
from flask_bootstrap import Bootstrap
from flask_login import (LoginManager, UserMixin, current_user, login_required, login_user,
                         logout_user)
from flask_migrate import Migrate
from flask_moment import Moment
from werkzeug.security import check_password_hash, generate_password_hash

from app import create_app, db
from app.main.forms import LoginForm, UserSignUpForm, userSignupInterestForm
from app.models import Event, EventInterest, Interest, Organizer, OrganizerInterest, User, UserEvents
from app.main.forms import LoginForm, UserSignUpForm
from app.main.organizers.OrganizerSignUpForm import OrganizerSignupForm
from flask import request, redirect
from app.main.event_form import EventForm
import uuid
from sqlalchemy import text

app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

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
        OrganizerInterest=OrganizerInterest,
        Organizer=Organizer,
        EventInterest=EventInterest,
        Event=Event,
    )

@app.route("/user/myAccount", methods=["GET", "POST"])
@login_required
def userMyAccount():
    return render_template("userMyAccount.html", name=current_user.name, email=current_user.email, faculty=current_user.faculty, major=current_user.major, campus=current_user.campus, yearOfStudy=current_user.yearOfStudy, interests=current_user.interests)


@app.route("/organizer/myAccount", methods=["GET", "POST"])
@login_required
def organizerMyAccount():
    print(current_user.role)
    return render_template("organizerMyAccount.html", name=current_user.organizer_name)


@app.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        role = request.form.get('role')  # Get the selected role from the form
        if current_user.is_authenticated:
            logout_user()
        print(current_user)
        if role == 'user':
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                print(f"User object: {user}")
                login_user(user)
                return redirect("/user/myAccount")  # Redirect to user's account
        elif role == 'organizer':
            organizer = Organizer.query.filter_by(organizer_email=email).first()
            print(f"Organizer object: {organizer}")
            if organizer and check_password_hash(organizer.password, password):
                login_user(organizer)
                return redirect("/organizer/myAccount")  # Redirect to organizer's account

        flash("Invalid email or password")

    return render_template("login.html", form=form)




@app.route("/user/signup", methods=["GET", "POST"])
def userSignup():
    form = UserSignUpForm()
    if form.validate_on_submit():
        email = User.query.filter_by(email=form.email.data).first()
        hashed_password = generate_password_hash(form.password.data)
        if email is None:
            if "utoronto" in form.email.data.split("@")[1]:
                user = User(
                    name=form.name.data,
                    email=form.email.data,
                    password=hashed_password,
                    faculty=form.faculty.data,
                    major=form.major.data,
                    campus=form.campus.data,
                    yearOfStudy=form.year_of_study.data,
                )
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect("/signup/interests")
            else:
                flash("You may only register with your UofT email")
        else:
            flash("Account with this email address already exists!")

    return render_template("index.html", form=form)

@app.route("/signup/interests", methods=["GET", "POST"])
@login_required
def signupInterests():
    form = userSignupInterestForm()
    form.interests.choices = [(interest.id, interest.name) for interest in Interest.query.all()]
    if request.method == 'POST' and form.validate_on_submit():
        for id in form.interests.data:
            user = User.query.filter_by(email=current_user.email).first()
            interest = Interest.query.filter_by(id=id).first()
            user.add_interest(interest)
            db.session.commit()
        return redirect("/user/myAccount")
    return render_template("interests.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/organizer/list", methods=["GET"])
def user_organizer_list():
    organizers = Organizer.query.all()
    if organizers is not None:
        return render_template("organizerDashboard.html",  organizers=organizers)

@app.route("/organizer/details/<int:organizer_id>", methods=["GET"])
def organizer_details(organizer_id):
    organizer = Organizer.query.filter_by(id = organizer_id).first()
    organizer_events = Event.query.filter_by(organization_id = organizer_id).all()
    return render_template("organizer-details.html", organization=organizer, organization_events = organizer_events)

@app.route("/organizer/signup", methods=["GET", "POST"])
def organizerSignup():
    form = OrganizerSignupForm()
    if form.validate_on_submit():
        organizer = Organizer.query.filter_by(organizer_name=form.organization_name.data).first()
        email = Organizer.query.filter_by(organizer_email=form.organization_email.data).first()
        hashed_password = generate_password_hash(form.password.data)
        if organizer is None and email is None:
            if "utoronto" in form.organization_email.data.split("@")[1]:
                image = form.image.data
                if image:
                    random_uuid = uuid.uuid4()
                    uuid_string = str(random_uuid)
                    image_path = 'app/resources/' + "event_" + uuid_string + ".jpg"
                    # You can process and save the image here, e.g., save it to a folder or a database.
                    image.save(image_path)
                else:
                    image_path = None
                organizer = Organizer(organizer_name=form.organization_name.data, 
                                      organizer_email=form.organization_email.data,
                                      password = hashed_password,
                                      description = form.organization_description.data,
                                      image_link = image_path,
                                      campus = form.organization_campus.data,
                                      website = form.organization_website_link.data,
                                      instagram = form.organization_instagram_link.data,
                                      linkedin = form.organization_linkedin_link.data)
                db.session.add(organizer)
                db.session.commit()
                login_user(organizer)
                return redirect("/organizer/myAccount")  # Redirect to the organizer's dashboard
            else:
                flash("You may only register with your UofT email")
        else:
            flash("Account with this email address already exists!")
    return render_template("index.html", form=form)


@app.route("/organizer/create/event", methods=["GET", "POST"])
@login_required
def organizer_create_event():
    form = EventForm()
    organizer = Organizer.query.filter_by(organizer_email=current_user.organizer_email).first()

    if form.validate_on_submit():
        organization_id = organizer.id
        event_name = Event.query.filter_by(event_name=form.event_name.data).first()
        if event_name is None:
            image = form.image.data
            if image:
                random_uuid = uuid.uuid4()
                uuid_string = str(random_uuid)
                image_path = 'app/resources/' + "event_" + uuid_string + ".jpg"
                # You can process and save the image here, e.g., save it to a folder or a database.
                image.save(image_path)
            else:
                image_path = None
            event_entry = Event(
                event_name=form.event_name.data,
                organization_id=organization_id,
                description=form.description.data,
                date=form.date.data,
                time=form.time.data,
                image_link = image_path,
                location=form.location.data,
                google_map_link=form.google_map_link.data,
                fee=form.fee.data,
                has_rsvp=form.has_rsvp.data,
                external_registration_link=form.external_registration_link.data,
            )

            db.session.add(event_entry)
            db.session.commit()
            return redirect("/organizer/myAccount")  # Redirect to the organizer's account after successful form submission

    return render_template("index.html", form=form)

@app.route("/event_details/<int:event_id>", methods=["GET"])
def event_details(event_id):
    # Assuming you have an Event model and it has a relationship with Organization
    event = Event.query.filter_by(id=event_id).first()

    if event:
        return render_template("event-details.html", event=event)
    else:
        # Handle the case where the event with the specified ID is not found
        return render_template("event_not_found.html")
    
@app.route("/myEvents", methods=["GET", "POST"])
@login_required
def myEvents():
    # Get the event IDs belonging to the current user


    user_event_ids = UserEvents.query.filter_by(user_id=current_user.id).values(text('event_id'))

    user_event_ids = [event_id[0] for event_id in user_event_ids]

    # Get the corresponding events from the Events table
    user_events = Event.query.filter(Event.id.in_(user_event_ids)).all()

    return render_template("my-events.html", user_events=user_events)



@app.route("/register_for_event/<int:event_id>", methods=["POST"])
@login_required
def register_for_event(event_id):
     # Add logic to register the user for the event in your database
     # Example: Add an entry to the user_event table with user id and event id
     if current_user.is_authenticated:
            if current_user.role == "user":
                # Assuming you have a UserEvent model and a current_user variable
                new_registration = UserEvents(user_id=current_user.id, event_id=event_id)
                db.session.add(new_registration)
                db.session.commit()

                # Add a flash message
                flash("You have successfully registered for the event!", "success")

     # Return a success response
     return redirect("user/myAccount")



if __name__ == "__main__":
    app.run()
