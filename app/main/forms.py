from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SelectField, StringField, SubmitField, validators, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Email, Optional

interests_dict = {
    1: "Academics",
    2: "Arts",
    3: "Athletics",
    4: "Recreation",
    5: "Community Service",
    6: "Culture & Identities",
    7: "Environment & Sustainability",
    8: "Global Interest",
    9: "Hobby & Leisure",
    10: "Leadership",
    11: "Media",
    12: "Politics",
    13: "Social",
    14: "Social Justices and Advocacy",
    15: "Spirituality & Faith Communities",
    16: "Student Governments, Councils & Unions",
    17: "Work & Career Development"
}

class UserSignUpForm(FlaskForm):
    name = StringField("What is your full name?", validators=[DataRequired()])
    email = EmailField("What is your UofT email address?", validators=[DataRequired(), Email()])
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
    submit = SubmitField("Next")


class LoginForm(FlaskForm):
    email = EmailField("What is your UofT email address?", validators=[DataRequired(), Email()])
    password = PasswordField("Enter your password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class userSignupInterestForm(FlaskForm):
    interests = MultiCheckboxField("Select Your Interests", choices=list(interests_dict.items()), validators=[Optional()], coerce=int)
    submit = SubmitField("Submit")   
