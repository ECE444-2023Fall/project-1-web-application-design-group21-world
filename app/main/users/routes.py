import uuid

from flask import current_app, flash, redirect, render_template, request, session, url_for
from flask_login import (current_user, login_required, login_user,
                         logout_user)
from werkzeug.security import check_password_hash, generate_password_hash



from ... import db
from ...models import (Event, EventInterests, Interest, Organizer, OrganizerEvents,
                        OrganizerInterests, User, UserEvents, UserInterests)
from ..forms import LoginForm, UserDetailsChangeForm, userSignupInterestForm, UserSignUpForm, OrganizerSignupForm
from . import users_blueprint


@users_blueprint.route("/create", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = User(
            name=request.json["name"],
            email=request.json["email"],
            password=request.json["password"],
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("users.user_list"))

    return render_template("index.html")


@users_blueprint.route("/list", methods=["GET"])
def user_list():
    users = User.query.all()
    if users is not None:
        return render_template("user.html", name=session.get("first_name", "Stranger"), users=users)

@users_blueprint.route("/user/myAccount", methods=["GET", "POST"])
@login_required
def userMyAccount():
    current_app.logger.info(current_user.role)
    form = UserDetailsChangeForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.faculty = form.faculty.data
        current_user.major = form.major.data
        current_user.campus = form.campus.data
        current_user.year_of_study = form.year_of_study.data
        db.session.commit()
        return redirect("/user/myAccount")
    form.name.data = current_user.name
    form.faculty.data = current_user.faculty
    form.major.data = current_user.major
    form.campus.data = current_user.campus 
    form.year_of_study.data = current_user.year_of_study
    return render_template("userMyAccount.html", form=form, name=current_user.name, email=current_user.email, interests=current_user.interests)


@users_blueprint.route("/user/signup", methods=["GET", "POST"])
def userSignup():
    form = UserSignUpForm()
    if form.is_submitted():
        if form.validate():
            email = User.query.filter_by(email=form.email.data).first()
            hashed_password = generate_password_hash(form.password.data)
            if email is None:
                if "utoronto" in form.email.data.split("@")[1]:
                    random_uuid = uuid.uuid4()
                    uuid_string = str(random_uuid)
                    user = User(
                        id = uuid_string,
                        name=form.name.data,
                        email=form.email.data,
                        password=hashed_password,
                        faculty=form.faculty.data,
                        major=form.major.data,
                        campus=form.campus.data,
                        year_of_study=form.year_of_study.data,
                    )
                    db.session.add(user)
                    db.session.commit()
                    login_user(user)
                    return redirect("/signup/interests")
                else:
                    flash("You may only register with your UofT email")
            else:
                flash("Account with this email address already exists!")
        else :
            print(form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'{field}: {error}', 'danger')

    return render_template("index.html", form=form)

@users_blueprint.route("/signup/interests", methods=["GET", "POST"])
@login_required
def signupInterests():
    form = userSignupInterestForm()
    form.interests.choices = [(interest.id, interest.name) for interest in Interest.query.all()]
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=current_user.email).first()
        all_interests = []
        if form.interests.data:
            for id in form.interests.data:
                interest = Interest.query.filter_by(id=id).first()
                all_interests.append(interest)
        user.update_interest(all_interests)    
        db.session.commit()
        return redirect("/user/myAccount")
    form.interests.default = [interest.id for interest in current_user.interests]
    form.process()
    return render_template("interests.html", form=form)