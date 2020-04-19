from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("LogIn")



class SignUpForm(FlaskForm):
    fName = StringField("Full Name", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=20, message="Minimum 8 characters"), EqualTo('cpassword', message="Passwords should match")])
    cpassword = PasswordField("Confirm Password", validators=[InputRequired()])
    submit = SubmitField("Sign Up")


