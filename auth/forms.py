from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, ValidationError, Length
from wtforms import StringField, PasswordField, SelectField, SubmitField, validators,BooleanField
from pharmbase.models import User, Role
from pharmbase import app, db


class RegForm(FlaskForm):
    first_name= StringField('First Name', [validators.DataRequired()])
    last_name = StringField('Last Name', [validators.DataRequired()])
    username= StringField('Username',[validators.length(min=5, max=15)])
    email = StringField('Email',
     [validators.Email(),
      validators.DataRequired(), 
      validators.Length(min=6, max=35)])
    password = PasswordField('Password', 
    [validators.DataRequired(), 
    validators.Length(min=3), 
    validators.EqualTo('confirm_pass', message='Passwords must match')])
    confirm_pass=PasswordField('Confirm Password')
   
    submit= SubmitField('Sign Up')

    def validate_username(self, username):
      user = User.query.filter_by(username=username.data).first()
      if user:
        raise ValidationError(f'{username.data} is already taken')

    
    def validate_email(self, email):
      user = User.query.filter_by(email=email.data).first()
      if user:
        raise ValidationError(f'Email already taken by registered user')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')