from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Your Username:', validators=[DataRequired()])
    password = PasswordField('Your Password:', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me?')
    submit = SubmitField('Sign In')
