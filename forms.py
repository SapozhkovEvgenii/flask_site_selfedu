from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email('Incorrect email')])
    password = PasswordField(
        "Password: ",
        validators=[
            DataRequired(),
            Length(min=8, max=100,
                   message="""Incorrect password.
                   You have to use 8 or more symbols""")])
    remember = BooleanField("Remainme", default=False)
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):

    """The class doesn't have field validators, because this functionality
    is implemented in the view 'register'"""

    name = StringField("Name: ")
    email = StringField("Email: ", )
    password = PasswordField("Password: ")
    password_repeat = PasswordField(
        "Repeat password: ")
    submit = SubmitField("Register")
