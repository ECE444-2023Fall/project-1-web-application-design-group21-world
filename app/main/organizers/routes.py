from flask import current_app, flash, redirect, render_template, request, session, url_for

from ... import db
from ...models import Organizer
from . import organizers_blueprint


@organizers_blueprint.route("/organizer/create", methods=["GET", "POST"])
def organizer_create():
    if request.method == "POST":
        print("REQUEST INFO", request.json)
        print("Hello Are you Amon!!")
        organizer = Organizer(
            organizer_name=request.json["organizer_name"],
            organizer_email=request.json["organizer_email"],
        )
        db.session.add(organizer)
        db.session.commit()
        return render_template("organizer.html", name=organizer.organizer_name, organizer=organizer)

    return render_template("index.html")


# @organizers_blueprint.route("/organizer/list", methods=["GET"])
# def organizer_list():
#     organizer = Organizer.query.all()
#     if organizer is not None:
#         return render_template("organizer.html", name=session.get("first_name", "Stranger"), organizer=organizer)
