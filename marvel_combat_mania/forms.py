from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class UserLoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    birthday = StringField('Birthday')
    password = PasswordField('Password', validators = [DataRequired()])
    submit_button = SubmitField()


class UserSigninForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit_button = SubmitField()