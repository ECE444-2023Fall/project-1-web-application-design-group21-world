from datetime import datetime

from flask import Flask, flash, logging, redirect, render_template, request, session, url_for
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField
from wtforms.validators import DataRequired, Email

from app import create_app, db
from app.models import Event, EventInterest, Interest, Organizer, OrganizerInterest, User

app = create_app()
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


class Form(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("What is your UofT email address?", validators=[DataRequired(), Email()])
    submit = SubmitField("Submit")


# @app.route("/",methods=['GET','POST'])
# def index():
# form = Form()
# if form.validate_on_submit():
#     # session['valid_email'] = False
#     old_name = session.get('name')
#     old_email = session.get('email')
#     old_username = session.get('username')
#     if old_name is not None and old_name != form.name.data:
#         flash('Looks like you have changed your name!')
#     if old_email is not None and old_email != form.email.data:
#         flash('Looks like you have changed your email!')
#     session['name'] = form.name.data
#     session['email'] = form.email.data
#     session['username'] = form.username.data
#     # if 'utoronto' in form.email.data.split("@")[1]:
#         # logger.log(form.email.data.split("@"))
#         # session['valid_email'] = True
#     return redirect(url_for('index'))


# return render_template('index.html', form=form, name=session.get('name'))
@app.route("/")
def index():
    try:
        users = users = db.session.execute(db.select(User).order_by(User.username)).scalars()

        user_text = "<ul>"
        for user in users:
            user_text += "<li>" + user.username + ", " + user.email + "</li>"
        user_text += "</ul>"
        return user_text
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = "<h1>Something is broken.</h1>"
        return hed + error_text


@app.route("/users")
def user_list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    return users


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
        organizer_name=request.args.get["organizer_name"],
        organizer_email=request.args.get["organizer_email"],
        description=request.args.get["description"],
        contact_email=request.args.get["contact_email"],
    )
    db.session.add(organizer)
    db.session.commit()
    return render_template("index.html")

@app.route("/organizer")
def organizer_list():
    organizers = db.session.execute(db.select(Organizer).order_by(Organizer.organizer_name)).scalars()
    return organizers

@app.route("/event/create", methods=["POST"])
def event_create():
    event = Event(
        event_name=request.args.get["event_name"],
        description=request.args.get["description"],
    )
    db.session.add(event)
    db.session.commit()
    return render_template("index.html")

@app.route("/event")
def event_list():
    events = db.session.execute(db.select(Event).order_by(Event.event_name)).scalars()
    return events


@app.route("/organizer/<int:id>", methods=["GET"])
def get_organizer(id):
    organizer = db.session.execute(db.select(Organizer).filter(Organizer.id == id)).scalar()
    return organizer


@app.route("/event/<int:id>", methods=["GET"])
def get_event(name):
    event = db.session.execute(db.select(Event).filter(Event.event_name == name)).scalar()
    return event


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
