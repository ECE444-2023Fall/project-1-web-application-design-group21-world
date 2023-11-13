import uuid

from flask import current_app, flash, redirect, render_template, request, session, url_for
from flask_login import (LoginManager, UserMixin, current_user, login_required, login_user,
                         logout_user)
from werkzeug.security import check_password_hash, generate_password_hash

from ... import db
from ...models import (Event, EventInterests, Interest, Organizer, OrganizerEvents,
                        OrganizerInterests, User, UserEvents, UserInterests)
from ..forms import LoginForm, UserDetailsChangeForm, userSignupInterestForm, UserSignUpForm, OrganizerSignupForm

from sqlalchemy.exc import IntegrityError

from . import organizers_blueprint


@organizers_blueprint.route("/organizer/create", methods=["GET", "POST"])
def organizer_create():
    if request.method == "POST":
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

@organizers_blueprint.route("/organizer/myAccount", methods=["GET", "POST"])
@login_required
def organizerMyAccount():
    current_app.logger.info(current_user.role)
    form = OrganizerDetailsChangeForm()
    if form.validate_on_submit():
        current_user.organizer_name = form.organization_name.data
        current_user.description = form.organization_description.data
        current_user.campus = form.organization_campus.data
        current_user.website = form.organization_website_link.data
        current_user.instagram = form.organization_instagram_link.data
        current_user.linkedin = form.organization_linkedin_link.data
        db.session.commit()
        return redirect("/organizer/myAccount")
    form.organization_name.data = current_user.organizer_name
    form.organization_description.data = current_user.description 
    form.organization_campus.data = current_user.campus
    form.organization_website_link.data = current_user.website
    form.organization_instagram_link.data = current_user.instagram
    form.organization_linkedin_link.data = current_user.linkedin
    return render_template("organizerMyAccount.html", form=form)


@organizers_blueprint.route("/organizer/list", methods=["GET"])
def user_organizer_list():
    organizers = Organizer.query.all()
    if organizers is not None:
        return render_template("organizerDashboard.html", organizers=organizers)


@organizers_blueprint.route("/organizer/details/<string:organizer_id>", methods=["GET"])
def organizer_details(organizer_id):
    organizer = Organizer.query.filter_by(id = organizer_id).first()
    return render_template(
        "organizer-details.html", organization=organizer, organization_events=organizer.events
    )


@organizers_blueprint.route("/organizer/signup", methods=["GET", "POST"])
def organizerSignup():
    form = OrganizerSignupForm()
    if form.is_submitted():
        if form.validate() is True:
            organizer = Organizer.query.filter_by(organizer_name=form.organization_name.data).first()
            email = Organizer.query.filter_by(organizer_email=form.organization_email.data).first()
            hashed_password = generate_password_hash(form.password.data)
            if organizer is None and email is None:
                if "utoronto" in form.organization_email.data.split("@")[1]:
                    image = form.image.data
                    if image:
                        random_uuid = uuid.uuid4()
                        uuid_string = str(random_uuid)
                        image_path = os.path.join(current_app.config["IMAGE_PATH_ORGANIZERS"], "organizer_" + uuid_string + "." + image.filename.split(".")[1])
                        # You can process and save the image here, e.g., save it to a folder or a database.
                        image.save(image_path)
                    else:
                        image_path = None
                    try:
                        organizer = Organizer(
                            id=str(uuid.uuid4()),
                            organizer_name=form.organization_name.data,
                            organizer_email=form.organization_email.data,
                            password=hashed_password,
                            description=form.organization_description.data,
                            image_link=image_path,
                            campus=form.organization_campus.data,
                            website=form.organization_website_link.data,
                            instagram=form.organization_instagram_link.data,
                            linkedin=form.organization_linkedin_link.data
                        )
                        db.session.add(organizer)
                        db.session.commit()
                        login_user(organizer)
                        return redirect("/organizer/myAccount")  # Redirect to the organizer's dashboard
                    except IntegrityError:
                        db.session.rollback()  # Rollback the transaction
                        flash("An error occurred. Please try again.", "danger")
                    login_user(organizer)
                    return redirect("/organizer/myAccount")  # Redirect to the organizer's dashboard
                else:
                    flash("You may only register with your UofT email")
            else:
                flash("Account with this email address already exists!", "danger")
        else :
            print(form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'{field}: {error}', 'danger')
    return render_template("index.html", form=form)