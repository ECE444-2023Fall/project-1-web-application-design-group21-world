
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash

from app.main.forms import LoginForm
from app.models import Organizer, User

from . import main


@main.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        role = request.form.get("role")  # Get the selected role from the form
        if current_user.is_authenticated:
            logout_user()
        print(current_user)
        if role == "user":
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                print(f"User object: {user}")
                login_user(user)
                return redirect(
                    "/user/myAccount"
                )  # Redirect to user's account
        elif role == "organizer":
            organizer = Organizer.query.filter_by(
                organizer_email=email
            ).first()
            print(f"Organizer object: {organizer}")
            if organizer and check_password_hash(organizer.password, password):
                login_user(organizer)
                return redirect(
                    "/organizer/myAccount"
                )  # Redirect to organizer's account

        flash("Invalid email or password")

    return render_template("login.html", form=form)


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))
