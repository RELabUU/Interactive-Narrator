#!/usr/bin/env python

from wtforms import Form, BooleanField
from wtforms import TextField, SubmitField, IntegerField, PasswordField
from wtforms import validators, ValidationError
from wtforms.validators import Length, required, DataRequired


class SetInfoForm(Form):
    # company_id = IntegerField('CompanyID', [validators.DataRequired("Please enter a valid name.")])
    # [required()])
    # company_name = TextField('Company Name', [Length(max=255), validators.DataRequired()])
    sprint_id = IntegerField('SprintID', [validators.DataRequired()])
    sprint_name = TextField('Sprint Name', [Length(max=255), validators.DataRequired(message='Please enter a valid name')])
    submit = SubmitField("Send")


class LoginForm(Form):
    username = TextField('Username', [Length(max=255), validators.DataRequired()])
    password = TextField('Password', [Length(max=255), validators.DataRequired()])
    submit = SubmitField("Login")


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    company_name = TextField('Company Name', [Length(max=255), validators.DataRequired()])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])
    submit = SubmitField("Register")

# if__name__ == '__main__':
