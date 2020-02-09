from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.validators import DataRequired
from app.datamodel import User

class LoginForm(FlaskForm):
    username = StringField('Your Username:', validators=[DataRequired()])
    password = PasswordField('Your Password:', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me?')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Your Username:', validators=[DataRequired()])
    email = StringField('Your Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password:', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
            
class BrowseForm(FlaskForm):
    q = StringField('Enter Query', default="")
    sortby = SelectField('Sort By:', choices = [(1, "Newest"),(2, "Oldest")], default = 1)
