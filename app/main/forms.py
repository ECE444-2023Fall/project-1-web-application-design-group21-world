from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SelectField, StringField, SubmitField, validators, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Email, Optional

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
    interests = MultiCheckboxField("Select Your Interests", choices=[], validators=[Optional()], coerce=int)
    submit = SubmitField("Submit")   
