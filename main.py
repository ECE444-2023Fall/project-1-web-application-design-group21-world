import json
import os
from datetime import datetime

from flask import (Flask, flash, logging, redirect, render_template, request,
                   session, url_for)
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_moment import Moment

from app import create_app, db
from app.models import (Event, EventInterest, Interest, Organizer,
                        OrganizerInterest, User)

app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, db)


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

@app.route("/users")
def user_list():
    try:
        users = User.query.all()
        return render_template("user.html", name=session['first_name'], users=users)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = "<h1>Something is broken.</h1>"
        return hed + error_text


@app.route("/users/create", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = User(
            username=request.args.get("username"),
            email=request.args.get("email"),
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("index.html")


@app.route("/user/<int:id>")
def user_detail(id):
    user = db.get_or_404(User, id)
    return render_template("user/detail.html", user=user)


@app.route("/organizer/create", methods=["POST"])
def organizer_create():
    organizer = Organizer(
        organizer_name=request.form["organizer_name"],
        organizer_email=request.form["organizer_email"],
        description=request.form["description"],
        contact_email=request.form["contact_email"],
        website=request.form["website"],
        instagram=request.form["instagram"],
        linkedin=request.form["linkedin"],
        campus=request.form["campus"],
    )
    db.session.add(organizer)
    db.session.commit()
    return render_template("organizer/create.html")


@app.route("/organizer/<int:id>", methods=["GET"])
def get_organizer(id):
    pass


# @app.route("/user/<int:id>/delete", methods=["GET", "POST"])
# def user_delete(id):
# 	user = db.get_or_404(User, id)
#     if request.method == "POST":
#         db.session.delete(user)
#         db.session.commit()
#         return redirect(url_for("user_list"))
#     return render_template("user/delete.html", user=user)

if __name__ == "__main__":
    app.run()
