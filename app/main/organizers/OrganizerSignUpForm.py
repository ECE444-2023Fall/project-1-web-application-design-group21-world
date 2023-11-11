from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed

from wtforms import (EmailField, FileField, PasswordField, SelectField, StringField, SubmitField,
                     validators)
from wtforms.validators import URL, DataRequired, Email, Length, Optional


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
    organization_instagram_link = StringField("Instagram Link", validators=[URL(), Optional()])

    submit = SubmitField("Submit")
