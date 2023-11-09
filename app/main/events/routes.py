from flask import render_template, request

from ... import db
from ...models import Event
from . import events_blueprint



@events_blueprint.route("/events/create", methods=["GET", "POST"])
def events_create():
    if request.method == "POST":
        print("REQUEST INFO", request.json)
        event = Event(
            event_name=request.json["event_name"],
            organizer_id=request.json["org_id"],
            description=request.json["description"],
            date=request.json["date"],
            time=request.json["time"],
            location=request.json["location"],
            google_map_link=request.json["google_map_link"],
            fee=request.json["fee"],
            has_rsvp=request.json["has_rsvp"],
            external_registration_link=request.json[
                "external_registration_link"
            ],
            external_registration_link=request.json["external_registration_link"],
        )
        db.session.add(event)
        db.session.commit()
        # print("URL FOUND", url_for("event.event_list"))
        # return redirect(url_for("event.event_list"))
        return render_template(
            "events_new.html", name=event.event_name, event=event
        )


# @events_blueprint.route("/events/list", methods=["GET"])
# def events_list():
#     events_list = Event.query.all()
#     if events_list is not None:
#         return render_template(
#             "events_list.html",
#             events_list=events_list,
#         )
