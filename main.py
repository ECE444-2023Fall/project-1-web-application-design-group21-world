import json
import os
from datetime import datetime

from flask import Flask, flash, logging, redirect, render_template, request, session, url_for
from flask_bootstrap import Bootstrap
from flask_login import (LoginManager, UserMixin, current_user, login_required, login_user,
                         logout_user)
from flask_migrate import Migrate
from flask_moment import Moment
from werkzeug.security import check_password_hash, generate_password_hash

from app import create_app, db
from app.main.forms import LoginForm, UserSignUpForm
from app.main.organizers.OrganizerSignUpForm import OrganizerSignupForm
from app.models import Event, EventInterest, Interest, Organizer, OrganizerInterest, User
from flask import request, redirect

app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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

@app.route("/userMyAccount", methods=["GET", "POST"])
@login_required
def userMyAccount():
    return render_template("userMyAccount.html", name = current_user.name,
        email=current_user.email,
        faculty=current_user.faculty,
        major=current_user.major,
        campus=current_user.campus,
        yearOfStudy=current_user.yearOfStudy,
    )

@app.route("/organizerMyAccount", methods=["GET", "POST"])
@login_required
def organizerMyAccount():
    return render_template("organizerMyAccount.html", name=session["organizer_name"])


@app.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        role = request.form.get('role')  # Get the selected role from the form

        if role == 'user':
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                print(f"User object: {user}")
                current_user = user
                login_user(user)
                return redirect("userMyAccount")  # Redirect to user's account
        elif role == 'organizer':
            organizer = Organizer.query.filter_by(organizer_email=email).first()
            print(f"Organizer object: {organizer}")
            if organizer and check_password_hash(organizer.password, password):
                session["organizer_name"] = organizer.organizer_name
                current_user = organizer
                login_user(organizer)
                return redirect("organizerMyAccount")  # Redirect to organizer's account

        flash("Invalid email or password")

    return render_template("login.html", form=form)




@app.route("/signup", methods=["GET", "POST"])
def signup():
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
                session["name"] = form.name.data
                session["email"] = form.email.data
                session["faculty"] = form.faculty.data
                session["major"] = form.major.data
                session["campus"] = form.campus.data
                session["yearOfStudy"] = form.year_of_study.data
                return redirect(url_for("users.user_list"))
            else:
                flash("You may only register with your UofT email")
        else:
            flash("Account with this email address already exists!")

    return render_template("index.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/organizer/dashboard", methods=["GET"])
def dashboard():
    return render_template("organizer_dashboard.html")


@app.route("/organizer/signup", methods=["GET", "POST"])
def organizerSignup():
    form = OrganizerSignupForm()
    if form.validate_on_submit():
        organizer = Organizer.query.filter_by(organizer_name=form.organization_name.data).first()
        email = Organizer.query.filter_by(organizer_email=form.organization_email.data).first()
        hashed_password = generate_password_hash(form.password.data)
        if organizer is None and email is None:
            if "utoronto" in form.organization_email.data.split("@")[1]:
                organizer = Organizer(organizer_name=form.organization_name.data, organizer_email=form.organization_email.data, password = hashed_password)
                db.session.add(organizer)
                db.session.commit()
                session["organizer_name"] = form.organization_name.data
                session["organizer_email"] = form.organization_email.data
                session["campus"] = form.organization_campus.data
                return redirect(url_for("organizers.organizer_list"))  # Redirect to the organizer's dashboard
            else:
                flash("You may only register with your UofT email")
        else:
            flash("Account with this email address already exists!")
    return render_template("index.html", form=form)


@app.cli.command("init_interests")
def init_interests():
    # List of interests to initialize
    interests_data = [
        "Academic",
        "Arts",
        "Athletics",
        "Recreation",
        "Community Service",
        "Culture & Identities",
        "Environment & Sustainability",
        "Global Interest",
        "Hobby & Leisure",
        "Leadership",
        "Media",
        "Politics",
        "Social",
        "Social Justice and Advocacy",
        "Spirituality & Faith Communities",
        "Student Governments, Councils & Unions",
        "Work & Career Development"
    ]

    with db.app.app_context():
        for interest_name in interests_data:
            interest = Interest(name=interest_name)
            db.session.add(interest)

        db.session.commit()


# @app.route("/user/<int:id>")
# def user_detail(id):
#     user = db.get_or_404(User, id)
#     return render_template("user/detail.html", user=user)


# @app.route("/organizer/create", methods=["POST"])
# def organizer_create():
#      organizer = Organizer(
#          organizer_name=request.form["organizer_name"],
#          organizer_email=request.form["organizer_email"],
#          description=request.form["description"],
#          contact_email=request.form["contact_email"],
#          website=request.form["website"],
#          instagram=request.form["instagram"],
#          linkedin=request.form["linkedin"],
#          campus=request.form["campus"],
#      )
#      db.session.add(organizer)
#      db.session.commit()
#      return render_template("organizer/create.html")


# @app.route("/organizer/<int:id>", methods=["GET"])
# def get_organizer(id):
#     pass


# @app.route("/user/<int:id>/delete", methods=["GET", "POST"])
# def user_delete(id):
# 	user = db.get_or_404(User, id)
#     if request.method == "POST":
#         db.session.delete(user)
#         db.session.commit()
#         return redirect(url_for("user_list"))
#     return render_template("user/delete.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)
