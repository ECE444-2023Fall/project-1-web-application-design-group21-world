from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SelectField, StringField, SubmitField, FileField, validators
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, Email, Length, URL, Optional

class OrganizerSignupForm(FlaskForm):
    organization_name = StringField("What is your Organization Name (*)?", validators=[DataRequired()])
    organization_email = EmailField("What is your Organization UofT Email Address? (*)", validators=[DataRequired(), Email()])
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
