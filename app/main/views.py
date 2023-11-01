from flask import (current_app, flash, redirect, render_template, session,
                   url_for)

from .. import db
from ..models import User
from . import main
from .forms import LoginForm


@main.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        email = User.query.filter_by(email=form.email.data).first()
            
        if user is None and email is None:
            if 'utoronto' in form.email.data.split("@")[1]:
                
                user = User(username=form.username.data, email=form.email.data)
                db.session.add(user)
                db.session.commit()
                session["first_name"] = form.first_name.data
                session["last_name"] = form.last_name.data
                session["email"] = form.email.data
                session["username"] = form.username.data
                return redirect(url_for("user_list"))
            else:
                flash("You may only register with your UofT email")
        else:
            flash('Account with this username/email address already exists!')
        
    return render_template("index.html", form=form)
            
        
