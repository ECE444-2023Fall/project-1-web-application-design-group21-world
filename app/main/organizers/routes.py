from flask import current_app, flash, redirect, render_template, request, session, url_for
from flask_login import (LoginManager, UserMixin, current_user, login_required, login_user,
                         logout_user)
from werkzeug.security import check_password_hash, generate_password_hash

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
        return redirect(url_for("organizers.dashboard"))

    return render_template("index.html")


@organizers_blueprint.route("/organizer/list", methods=["GET"])
def organizer_list():
    organizers = Organizer.query.all()
    if organizers is not None:
        return render_template(
            "organizerDashboard.html",
            name=session.get("organization_name", "Stranger"),
            organizers=organizers,
        )
