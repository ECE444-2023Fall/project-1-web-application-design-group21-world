from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SelectField, StringField, SubmitField, validators
from wtforms.validators import DataRequired, Email, Length

class OrganizerSignupForm(FlaskForm):
    organization_name = StringField("What is your organization name?", validators=[DataRequired()])
    organization_email = EmailField("What is your organization UofT email address?", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Enter your password",
        validators=[
            DataRequired(),
            validators.Length(min=8, max=80),
            validators.EqualTo("confirm", message="Passwords must match"),
        ],
    )
    confirm_password = PasswordField("Repeat password")
    organization_campus = SelectField(
        "Campus",
        choices=[("UTSG"), ("UTSC"), ("UTM")],
        validators=[DataRequired()],
    )
    organization_description = StringField("Organization Description", validators=[Length(max=500)])
    organization_website_link = StringField("Website Link")
    organization_instagram_link = StringField("Instagram Link")
    organization_linkedin_link = StringField("LinkedIn Link")

    submit = SubmitField("Submit")
