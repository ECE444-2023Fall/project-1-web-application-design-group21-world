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
        choices=[("Engineering", "Applied science and engineering"), 
                 ("Architecture", "Architecture, landscape and design"), ("ArtSci", "Arts and Science"), 
                 ("ContStd", " Continuing studies"), ("dentistry", "Dentistry"), ("Edu", "Education"), 
                 ("Info", "Information"), ("Kinesology", "Kinesiology and physical education"), 
                 ("Law", "Law"), ("Management", "Management"), ("Med", "Medicine"), ("Music", "Music"), 
                 ("Nursing", "Nursing"), ("Pharmacy", "Pharmacy"), ("PubHealth", "Public Health"), 
                 ("SocialWork", "Social Work"), ("Anthro", "Anthroplogy"), ("Bio", "Biology"), 
                 ("ChemandPhy", "Chemical and Physical Sciences"), ("Eco", "Economics"), 
                 ("English", "English and Drama"), ("Geography", "Geography"), ("Hist", "Historical Studies"), 
                 ("ICCIT", "Instituute of Communication, Culture, Information and Technology (ICCIT)"), 
                 ("Lang", "Language Studies"), ("Management", "Management"), 
                 ("Math", "Mathematical and Computational Sciences"), ("Philo", "Philosophy"), 
                 ("PolSci", "Political Science"), ("Psych", "Psychology"), ("Socio", "Sociology"), 
                 ("VisStd", "Visual Studies"), ("Arts", "Arts"), ("Sci", "Science")],
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
