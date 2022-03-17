from calendar import c
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, PasswordField, SelectField, BooleanField
from wtforms.validators import InputRequired, Optional, Email, NumberRange, Length


class RegisterUserForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    email = StringField(
        "User Email",
        validators=[InputRequired(), Email(), Length(max=50)]
    )
    first_name = StringField(
        "First name",
        validators=[InputRequired(), Length(max=30)],
    )
    last_name = StringField(
        "Last name",
        validators=[InputRequired(), Length(max=30)],
    )


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=1, max=20)],
    )


class FeedbackForm(FlaskForm):
    title = StringField(
        "Feedback Title",
        validators=[InputRequired(), Length(min=1, max=100)],
    )
    content = TextAreaField(
        "Feedback Content",
        validators=[InputRequired()],
    )
