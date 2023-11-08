from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SelectField, StringField, SubmitField, validators, SelectMultipleField
from wtforms.validators import DataRequired, Email


class UserSignUpForm(FlaskForm):
    name = StringField("What is your full name?", validators=[DataRequired()])
    email = EmailField(
        "What is your UofT email address?",
        validators=[DataRequired(), Email()],
    )
    password = PasswordField(
        "Enter your password",
        validators=[
            DataRequired(),
            validators.Length(min=8, max=80),
            validators.EqualTo("confirm", message="Passwords must match"),
        ],
    )
    confirm = PasswordField("Repeat passoword")
    faculty = SelectField(
        "Faculty",
        choices=[
            ("Commerce", "Rotman"),
            ("Engineering", "Eng"),
            ("ArtSci", "A&S"),
        ],
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
    submit = SubmitField("Next")


class LoginForm(FlaskForm):
    email = EmailField(
        "What is your UofT email address?",
        validators=[DataRequired(), Email()],
    )
    password = PasswordField(
        "Enter your password", validators=[DataRequired()]
    )
    submit = SubmitField("Submit")

class userSignupInterestForm(FlaskForm):
    userInterests = SelectMultipleField(
        "Interests",
        choices=[("Academics"), ("Arts"), ("Athletics"), ("Recreation"), ("Community Service"), ("Culture & Identities"),
                 ("Environment & Sustainability"), ("Global Interest"), ("Hobby & Leisure"), ("Leadership"), ("Media"), 
                 ("Politics"), ("Social"), ("Social Justics and Advocacy"), ("Spirituality & Faith Communities"), 
                 ("Student Governments, Councils & Unions"), ("Work & Career Development")], 
        validators=[DataRequired()],         
    )
    Submit = SubmitField("Submit")
                                    
