import uuid
import os

from flask import current_app, flash, redirect, render_template, request, session, url_for
from flask_login import login_required, current_user

from ...models import (Event, EventInterests, Interest, Organizer, OrganizerEvents,
                        OrganizerInterests, User, UserEvents, UserInterests)
from ..forms import LoginForm, UserDetailsChangeForm, userSignupInterestForm, UserSignUpForm, OrganizerSignupForm, EventForm, eventInterestForm
from ... import db
from ...models import Event
from . import events_blueprint


@events_blueprint.route("/events/create", methods=["GET", "POST"])
def events_create():
    if request.method == "POST":
        event = Event(
            event_name=request.json["event_name"],
            organizer_id=request.json["organizer_id"],
            description=request.json["description"],
            date=request.json["date"],
            time=request.json["time"],
            location=request.json["location"],
            google_map_link=request.json["google_map_link"],
            fee=request.json["fee"],
            #has_rsvp=request.json["has_rsvp"],
            external_registration_link=request.json["external_registration_link"],
        )
        db.session.add(event)
        db.session.commit()
        return render_template("events_new.html", name=event.event_name, event=event)
    return render_template("index_event.html")

@events_blueprint.route("/organizer/create/event", methods=["GET", "POST"])
@login_required
def organizer_create_event():
    form = EventForm()
    if form.validate_on_submit():
        event_name = Event.query.filter_by(event_name=form.event_name.data).first()
        if event_name is None:
            image = form.image.data
            if image:
                random_uuid = uuid.uuid4()
                uuid_string = str(random_uuid)
                image_path = os.path.join(current_app.config["IMAGE_PATH_EVENTS"],"event_" + uuid_string + "." + image.filename.split(".")[1])
                # You can process and save the image here, e.g., save it to a folder or a database.
                image.save(image_path)
            else:
                image_path = None
            event_entry = Event(
                event_name=form.event_name.data,
                organizer_id=current_user.id,
                description=form.description.data,
                date=form.date.data,
                time=form.time.data,
                image_link=image_path,
                location=form.location.data,
                google_map_link=form.google_map_link.data,
                fee=form.fee.data,
                #has_rsvp=form.has_rsvp.data,
                external_registration_link=form.external_registration_link.data,
            )
            current_user.add_event(event_entry)
            db.session.add(event_entry)
            db.session.commit()
            session['event_id'] = event_entry.id
            return redirect("/organizer/create/event/interests")
    else :
            print(form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'{field}: {error}', 'danger')  # Redirect to the organizer's account after successful form submission

    return render_template("index.html", form=form)

@events_blueprint.route("/organizer/create/event/interests", methods=["GET", "POST"])
@login_required
def eventInterests():
    form = eventInterestForm()
    form.interests.choices = [(interest.id, interest.name) for interest in Interest.query.all()]
    if request.method == 'POST' and form.validate_on_submit():
        for id in form.interests.data:
            #print(session)
            event = Event.query.filter_by(id=session['event_id']).first()
            interest = Interest.query.filter_by(id=id).first()
            event.add_interest(interest)
            db.session.commit()
        session.pop('event_id')
        return redirect("/organizer/myAccount")
    return render_template("interests_events.html", form=form)

@events_blueprint.route("/event_details/<int:event_id>", methods=["GET"])
def event_details(event_id):
    # Assuming you have an Event model and it has a relationship with Organization
    event = Event.query.filter_by(id=event_id).first()

    if (event.image_link is None):
        event.image_link = "/static/assets/default_event_image.jpg"

    if event:
        return render_template("event-details.html", event=event)
    else:
        # Handle the case where the event with the specified ID is not found
        return render_template("event_not_found.html")


@events_blueprint.route("/myEvents", methods=["GET"])
@login_required
def myEvents():
    if current_user.is_authenticated:
        if current_user.role == "user":
            eventIntID_query = db.session.query(EventInterests).all() #remove session here?
            eventIntID = {item.interest_id for item in eventIntID_query}
            userIntID_query = db.session.query(UserInterests).filter_by(user_id=current_user.id).all()
            userIntID = {item.interest_id for item in userIntID_query}
            common = eventIntID.intersection(userIntID)
            if common:
                event_query = db.session.query(EventInterests.c.event_id).filter(EventInterests.c.interest_id.in_(common)).all()
                event_ids = [event_id for(event_id,) in event_query]
                events = db.session.query(Event).filter(Event.id.in_(event_ids)).all()
                return render_template("events_rec.html", user_events=current_user.events,u_id=events)
            else:
                return render_template("events_rec.html", user_events=current_user.events)
        elif current_user.role == "organizer":
            return render_template("events_rec.html", user_events=current_user.events)

@events_blueprint.route("/discover", methods=["GET", "POST"])
def allEvents():
    current_app.logger.info(f"EVENTS: {Event.query.all()}")
    return render_template("events.html", events=Event.query.all())

@events_blueprint.route("/register_for_event/<int:event_id>", methods=["POST"])
@login_required
def register_for_event(event_id):
    event = Event.query.get(event_id)

    if current_user.is_authenticated:
        if current_user.role == "user":
            if request.method == "POST":
                # Assuming you have a UserEvent model and a current_user variable
                current_app.logger.info(f"Current Role {current_user.role}")
                current_user.add_event(event)
                db.session.add(current_user)
                db.session.commit()
                flash("You have successfully registered for the event!", "success")
            elif request.method == "DELETE":
                current_app.logger.info(f"Current Role {current_user.role}")
                current_user.remove_event(event)
                db.session.add(current_user)
                db.session.commit()
                flash("You have successfully unregistered for the event!", "success")
    
    return redirect(url_for("events.event_details", event_id=event.id))

@events_blueprint.route("/unregister_for_event/<int:event_id>", methods=["POST"])
@login_required
def unregister_for_event(event_id):
    event = Event.query.get(event_id)

    if current_user.is_authenticated:
        if current_user.role == "user":
            if request.method == "POST":
                current_app.logger.info(f"Current Role {current_user.role}")
                current_user.remove_event(event)
                db.session.add(current_user)
                db.session.commit()
                flash("You have successfully unregistered for the event!", "success")
    
    return redirect(url_for("events.event_details", event_id=event.id))