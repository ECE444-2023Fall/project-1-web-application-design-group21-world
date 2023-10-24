
from datetime import datetime
from app import create_app, db
# from app.models import User, Role
from app.models import Organizer, OrganizerInterest
from flask import Flask, redirect, render_template, session, url_for, flash, logging
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField
from wtforms.validators import DataRequired, Email
app = Flask(__name__,static_folder='app/static',template_folder='app/templates',)
logger = logging.create_logger(app)
app.config["SECRET_KEY"] = "shhhh ... "
bootstrap = Bootstrap(app)
moment = Moment(app)

class Form(FlaskForm):
    name = StringField('What is your name?',validators=[DataRequired()])
    # email = EmailField('What is your UofT email address?',validators=[DataRequired(),Email()])
    submit = SubmitField('Submit')


@app.route("/",methods=['GET','POST'])
def index():
    form = Form()
    if form.validate_on_submit():
        # session['valid_email'] = False
        old_name = session.get('name')
        # # old_email = session.get('email')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        # # # if old_email is not None and old_email != form.email.data:
            # flash('Looks like you have changed your email!')
        session['name'] = form.name.data
        # # session['email'] = form.email.data
        # if 'utoronto' in form.email.data.split("@")[1]:
            # logger.log(form.email.data.split("@"))
            # session['valid_email'] = True
        return redirect(url_for('index'))
    
    return render_template('index.html', form=form, name=session.get('name'))

@app.route("/users")
def user_list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    return users

@app.route("/users/create", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            email=request.form["email"],
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user_detail", id=user.id))
    return render_template("user/create.html")

@app.route("/user/<int:id>")
def user_detail(id):
    user = db.get_or_404(User, id)
    return render_template("user/detail.html", user=user)

@app.route("/organizer/create", methods=["POST"])
def organizer_create():
    organizer = Organizer(
        organizer_name = request.form["organizer_name"]
        organizer_email = request.form["organizer_email"]
        description = request.form["description"]
        contact_email = request.form["contact_email"]
        website = request.form["website"]
        instagram = request.form["instagram"]
        linkedin = request.form["linkedin"]
        campus = request.form["campus"]
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

# if __name__ == '__main__':
#     app.run()
