#!/usr/bin/env python

from wtforms import Form, BooleanField
from wtforms import StringField, SubmitField, IntegerField, PasswordField
from wtforms import validators, ValidationError
from wtforms.validators import Length, required, DataRequired


class SetInfoForm(Form):
    # company_id = IntegerField('CompanyID', [validators.DataRequired("Please enter a valid name.")])
    # [required()])
    # company_name = StringField('Company Name', [Length(max=255), validators.DataRequired()])
    # sprint_id = IntegerField('SprintID', [validators.DataRequired()])
    sprint_name = StringField('Sprint Name', [Length(max=255),
                                              validators.DataRequired(message='Please enter a valid name')])
    submit = SubmitField("Send")
    # Regexp(r'^[\w.@+-]+$')
    # validators.Regexp(r'^[a-zA-Z0-9_ ]*$'),
class LoginForm(Form):
    username = StringField('Username', [Length(max=255), validators.DataRequired()])
    password = PasswordField('Password', [Length(max=255), validators.DataRequired(message='wrong')])
    remember = BooleanField('Remember me', default=False)
    submit = SubmitField("Login")


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=20)])
    company_name = StringField('Company Name', [Length(max=255), validators.DataRequired()])
    email = StringField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    # accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])
    submit = SubmitField("Register")

# if__name__ == '__main__':
