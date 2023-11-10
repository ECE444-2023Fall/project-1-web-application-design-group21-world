from flask_wtf import FlaskForm
from wtforms.fields import DateField, DateTimeField
from wtforms_components import TimeField
from wtforms import FileField, StringField, SubmitField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, Email, Length, URL
from wtforms import SelectMultipleField

class EventForm(FlaskForm):
    event_name = StringField("Event Name", validators=[DataRequired()])
    org_id = StringField("Organization ID", validators=[DataRequired()])
    description = StringField("Event Description", validators=[DataRequired(), Length(max=500)])
    date = DateField("Date of Event", format='%Y-%m-%d', validators=[DataRequired()])
    time = StringField("Time of Event", validators=[DataRequired()])
    #time = TimeField("Time of Event", format='%H:%M', validators=[DataRequired()])
    image = FileField("Upload Event Image", validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    location = StringField("Location of Event", validators=[DataRequired()])
    google_map_link = StringField("Map of Event", validators=[DataRequired(), URL()])
    fee = StringField("Fee for Event")
    has_rsvp = StringField("RSVP Button?", validators=[DataRequired()])
    external_registration_link = StringField("Link of Registration")

    #choices = [('Academic', 'Academic'), ('Arts', 'Arts'), ('Athletics', 'Athletics'),('Recreation', 'Recreation'),
               #('Community Service','Community Service'),('Culture & Identities', 'Culture & Identities'),
               #('Environment & Sustainability', 'Environment & Sustainability'), ('Global Interest','Global Interest'),
               #('Hobby & Leisure','Hobby & Leisure'), ('Leadership', 'Leadership'), ('Media', 'Media'), ('Politics', 'Politics'),
               #('Social','Social'), ('Social Justice and Advocacy','Social Justice and Advocacy'), ('Spirituality & Faith Communities','Spirituality & Faith Communities'),
               #('Student Governments, Councils & Unions' , 'Student Governments, Councils & Unions'), ('Work & Career Development', 'Work & Career Development')]
    
    #selected_interests = SelectMultipleField('Select the Event Interest Areas', choices=choices)
    
    submit = SubmitField("Submit")
