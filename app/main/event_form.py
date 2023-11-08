from flask_wtf import FlaskForm
from wtforms import FileField, StringField, SubmitField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, Email


class EventForm(FlaskForm):
    event_name = StringField("Event Name", validators=[DataRequired()])
    org_id = StringField("Organization ID", validators=[DataRequired()])
    description = StringField("Event Description", validators=[DataRequired()])
    date = StringField("Date of Event", validators=[DataRequired()])
    time = StringField("Time of Event", validators=[DataRequired()])
    image = FileField("Upload Event Image", validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    location = StringField("Location of Event", validators=[DataRequired()])
    google_map_link = StringField("Map of Event", validators=[DataRequired()])
    fee = StringField("Fee for Event")
    has_rsvp = StringField("RSVP Button?", validators=[DataRequired()])
    external_registration_link = StringField("Link of Registration")
    submit = SubmitField("Submit")
