from flask import (
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from ... import db
from ...models import User
from ..forms import LoginForm
from . import users_blueprint


@users_blueprint.route("/create", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        print("REQUEST INFO", request.json)
        user = User(
            name=request.json["name"],
            email=request.json["email"],
            password=request.json["password"],
        )
        db.session.add(user)
        db.session.commit()
        print("URL FOUND", url_for("users.user_list"))
        return redirect(url_for("users.user_list"))

    return render_template("index.html")


@users_blueprint.route("/list", methods=["GET"])
def user_list():
    users = User.query.all()
    if users is not None:
        return render_template(
            "user.html",
            name=session.get("first_name", "Stranger"),
            users=users,
        )
