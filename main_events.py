# import os

# from flask import flash, render_template, session
# from flask_migrate import Migrate

# from app import create_app, db
# from app.main.event_form import EventForm
# from app.models import (Event, EventInterest, Interest, Organizer,
#                         OrganizerInterest, User)

# app = create_app(os.getenv("FLASK_CONFIG") or "default")
# migrate = Migrate(app, db)


# @app.shell_context_processor
# def make_shell_context():
#     return dict(
#         db=db,
#         User=User,
#         Interest=Interest,
#         OrganizerInterest=OrganizerInterest,
#         Organizer=Organizer,
#         EventInterest=EventInterest,
#         Event=Event,
#     )


# @app.route("/", methods=["GET", "POST"])
# def event_index():
#     form = EventForm()
#     if form.validate_on_submit():
#         event_name = Event.query.filter_by(
#             event_name=form.event_name.data
#         ).first()
#         if event_name is None:
#             event_entry = Event(
#                 event_name=form.event_name.data,
#                 organizer_id=form.org_id.data,
#                 description=form.description.data,
#                 date=form.date.data,
#                 time=form.time.data,
#                 location=form.location.data,
#                 google_map_link=form.google_map_link.data,
#                 fee=form.fee.data,
#                 has_rsvp=form.has_rsvp.data,
#                 external_registration_link=form.external_registration_link.data,
#             )
#             db.session.add(event_entry)
#             db.session.commit()
#             session["event_name"] = form.event_name.data
#             session["organizer_id"] = form.org_id.data
#             session["description"] = form.description.data
#             session["date"] = form.date.data
#             session["time"] = form.time.data
#             session["location"] = form.location.data
#             session["google_map_link"] = form.google_map_link.data
#             session["fee"] = form.fee.data
#             session["has_rsvp"] = form.has_rsvp.data
#             session[
#                 "external_registration_link"
#             ] = form.external_registration_link.data
#         # email = Event.query.filter_by(email=form.email.data).first()

#         # if event_name is None and email is None:
#         #    if "utoronto" in form.email.data.split("@")[1]:
#         #        event_name = Event(event_name=form.username.data, email=form.email.data)
#         #        db.session.add(event_name)
#         #        db.session.commit()
#         #        session["email"] = form.email.data
#         #        session["event_name"] = form.username.data
#         #        return redirect(url_for("event.event_list"))
#         #    else:
#         #        flash("You may only register with your UofT email")
#         # else:
#         #    flash("Account with this username/email add
#         # ress already exists!")
#         else:
#             flash("Account with this username already exists!")

#     return render_template("index_event.html", form=form)


# # @app.route("/user/<int:id>")
# # def user_detail(id):
# #     user = db.get_or_404(User, id)
# #     return render_template("user/detail.html", user=user)


# # @app.route("/organizer/create", methods=["POST"])
# # def organizer_create():
# #      organizer = Organizer(
# #          organizer_name=request.form["organizer_name"],
# #          organizer_email=request.form["organizer_email"],
# #          description=request.form["description"],
# #          contact_email=request.form["contact_email"],
# #          website=request.form["website"],
# #          instagram=request.form["instagram"],
# #          linkedin=request.form["linkedin"],
# #          campus=request.form["campus"],
# #      )
# #      db.session.add(organizer)
# #      db.session.commit()
# #      return render_template("organizer/create.html")


# # @app.route("/organizer/<int:id>", methods=["GET"])
# # def get_organizer(id):
# #     pass


# # @app.route("/user/<int:id>/delete", methods=["GET", "POST"])
# # def user_delete(id):
# # 	user = db.get_or_404(User, id)
# #     if request.method == "POST":
# #         db.session.delete(user)
# #         db.session.commit()
# #         return redirect(url_for("user_list"))
# #     return render_template("user/delete.html", user=user)

# # if __name__ == "__main__":
# #    app.run()
