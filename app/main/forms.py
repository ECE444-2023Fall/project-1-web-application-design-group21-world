from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    first_name = StringField("What is your first name?", validators=[DataRequired()])
    last_name = StringField("What is your last name?", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField(
        "What is your UofT email address?", validators=[DataRequired(), Email()]
    )
    submit = SubmitField("Submit")
