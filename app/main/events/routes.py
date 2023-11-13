from flask import current_app, flash, redirect, render_template, request, session, url_for

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
            has_rsvp=request.json["has_rsvp"],
            external_registration_link=request.json["external_registration_link"],
        )
        db.session.add(event)
        db.session.commit()
        return render_template("events_new.html", name=event.event_name, event=event)
    return render_template("index_event.html")
