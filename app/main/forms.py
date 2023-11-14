from flask_wtf import FlaskForm
from wtforms import DateField, DateTimeField, FileField, StringField, SubmitField, SelectMultipleField, widgets
from flask_wtf.file import FileAllowed
from wtforms import (EmailField, PasswordField, SelectField, SelectMultipleField, StringField,
                     SubmitField, validators, widgets, FileField)
from wtforms.validators import DataRequired, Email, Optional, Length, URL

class UserDetailsChangeForm(FlaskForm):
    name = StringField("What is your full name?", validators=[DataRequired()])
    faculty = SelectField(
        "Faculty",
        choices=[("Commerce", "Rotman"), ("Engineering", "Eng"), ("ArtSci", "A&S")],
        validators=[DataRequired()],
    )
    major = StringField("Major", validators=[DataRequired()])
    campus = SelectField(
        "Campus",
        choices=[("St. George"), ("Scarborough"), ("Missasauga")],
        validators=[DataRequired()],
    )
    year_of_study = SelectField(
        "Year of Study",
        choices=[("1st"), ("2nd"), ("3rd"), ("4th"), ("5th"), ("Masters"), ("PhD"), ("other")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Modify")

class UserSignUpForm(FlaskForm):
    name = StringField("What is your Full Name?", validators=[DataRequired()])
    email = EmailField("What is your UofT Email Address?", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Enter your Password (*)",
        validators=[
            DataRequired(),
            validators.Length(min=8, max=80),
            validators.EqualTo("confirm", message="Passwords must match"),
        ],
    )
    confirm = PasswordField("Repeat Password (*)")
    faculty = SelectField(
        "Faculty (*)",
        choices=[("Commerce", "Rotman"), ("Engineering", "Eng"), ("ArtSci", "A&S")],
        validators=[DataRequired()],
    )
    major = StringField("Major (*)", validators=[DataRequired()])
    campus = SelectField(
        "Campus (*)",
        choices=[("St. George"), ("Scarborough"), ("Missasauga")],
        validators=[DataRequired()],
    )
    year_of_study = SelectField(
        "Year of Study (*)",
        choices=[("1st"), ("2nd"), ("3rd"), ("4th"), ("5th"), ("Masters"), ("PhD"), ("other")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Next")


class LoginForm(FlaskForm):
    email = EmailField("What is your UofT Email Address?", validators=[DataRequired(), Email()])
    password = PasswordField("Enter your Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class userSignupInterestForm(FlaskForm):
    interests = MultiCheckboxField(
        "Select Your Interests", choices=[], validators=[Optional()], coerce=int
    )
    submit = SubmitField("Submit")

class OrganizerSignupForm(FlaskForm):
    organization_name = StringField("What is your organization name?", validators=[DataRequired()])
    organization_email = EmailField(
        "What is your organization UofT email address?", validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Enter your password (*)",
        validators=[
            DataRequired(),
            validators.Length(min=8, max=80),
            validators.EqualTo("confirm", message="Passwords must match"),
        ],
    )
    confirm = PasswordField("Repeat Password (*)")
    organization_campus = SelectField(
        "Campus",
        choices=[("St. George"), ("Scarborough"), ("Missasauga")],
        validators=[DataRequired()],
    )
    image = FileField("Upload Organizer Image (*)", validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    organization_description = StringField("Organization Description (*)", validators=[Length(max=500)])
    organization_website_link = StringField("Website Link", validators=[URL(), Optional()])
    organization_instagram_link = StringField("Instagram Link", validators=[URL(), Optional()])
    organization_linkedin_link = StringField("LinkedIn Link", validators=[URL(), Optional()])

    submit = SubmitField("Submit")

class OrganizerDetailsChangeForm(FlaskForm):
    organization_name = StringField("What is your organization name?", validators=[DataRequired()])
    organization_campus = SelectField(
            "Campus",
            choices=[("St. George"), ("Scarborough"), ("Missasauga")],
            validators=[DataRequired()],
        )
    organization_description = StringField("Organization Description (*)", validators=[Length(max=500)])
    organization_website_link = StringField("Website Link", validators=[URL(), Optional()])
    organization_instagram_link = StringField("Instagram Link", validators=[URL(), Optional()])
    organization_linkedin_link = StringField("LinkedIn Link", validators=[URL(), Optional()])
    submit = SubmitField("Modify")

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
    #has_rsvp = StringField("RSVP Button?", validators=[DataRequired()])
    external_registration_link = StringField("Link of Registration", validators=[Optional(), URL()])
    submit = SubmitField("Submit")

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class eventInterestForm(FlaskForm):
    interests = MultiCheckboxField("Select Your Event's Target Interest Area", choices=[], validators=[Optional()], coerce=int)
    submit = SubmitField("Submit")   
