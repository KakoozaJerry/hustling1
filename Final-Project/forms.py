from flask_wtf import Form
from wtforms import SubmitField, StringField, PasswordField,BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_wtf import FlaskForm

class Login(FlaskForm):
    email = StringField('User Name', validators=[InputRequired(message="Please enter your email to log in"), Email])
    password = PasswordField('Password', validators=[InputRequired(message="Please enter your password")])
    login = SubmitField('Log In')
class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])