from flask_wtf import FlaskForm
from wtforms import DateField, DateTimeField, FileField, StringField, SubmitField, SelectMultipleField, widgets
from wtforms_components import TimeField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, Email, Length, URL, Optional, NumberRange
from datetime import datetime, time 

class EventForm(FlaskForm):
    event_name = StringField("Event Name", validators=[DataRequired()])
    description = StringField("Event Description", validators=[Optional(), Length(max=500)])
    date = DateField("Date of Event", format='%Y-%m-%d', validators=[DataRequired()])
    time = StringField("Time of Event", validators=[DataRequired()])
    #time = TimeField("Time of Event", format='%HH:%MM', validators=[DataRequired()])
    image = FileField("Upload Event Image", validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    location = StringField("Location of Event", validators=[DataRequired()])
    google_map_link = StringField("Map of Event", validators=[Optional(), URL()])
    fee = StringField("Fee for Event", validators=[Optional()])#,NumberRange(min=1, max=500)])
    has_rsvp = StringField("RSVP Button?", validators=[DataRequired()])
    external_registration_link = StringField("Link of Registration", validators=[Optional(), URL()])
    submit = SubmitField("Submit")

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class eventInterestForm(FlaskForm):
    interests = MultiCheckboxField("Select Your Event's Target Interest Area", choices=[], validators=[Optional()], coerce=int)
    submit = SubmitField("Submit")   


