from flask_wtf import FlaskForm
from wtforms import (EmailField, PasswordField, SelectField, SelectMultipleField, StringField,
                     SubmitField, validators, widgets)
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
