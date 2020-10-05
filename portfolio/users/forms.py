from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from portfolio.models import User


# form class to register user
class RegistrationForm(FlaskForm):
    # form fields and validation checks for fields
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # check if username in databse
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first() # get first user with same username
        if user: # check if true
            # raise validation message
            raise ValidationError('That username is taken. Please choose a different one.')

    # check if email in databse
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first() # get first user with same email
        if user: # check if true
            # raise validation message
            raise ValidationError('That email is taken. Please choose a different one.')


# form class to login user
class LoginForm(FlaskForm):
    # form fields and validation checks for fields
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# form class to update user account
class UpdateAccountForm(FlaskForm):
    # form fields and validation checks for fields
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    # check if username in databse
    def validate_username(self, username):
        if username.data != current_user.username: # check username not current user
            user = User.query.filter_by(username=username.data).first() # get first user with same username
            if user: # check if true
                # raise validation message
                raise ValidationError('That username is taken. Please choose a different one.')

    # check if email in databse
    def validate_email(self, email):
        if email.data != current_user.email: # check email not current user
            user = User.query.filter_by(email=email.data).first() # get first user with same email
            if user: # check if true
                # raise validation message
                raise ValidationError('That email is taken. Please choose a different one.')

# form class to reset user email
class RequestResetForm(FlaskForm):
    # form fields and validation checks for fields
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    # check if email in databse
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first() # get first user with same email
        if user is None: # check if true
            # raise validation message
            raise ValidationError('There is no account with that email. You must register first.')

# form class to reset user email
class ResetPasswordForm(FlaskForm):
    # form fields and validation checks for fields
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


