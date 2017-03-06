#!/usr/bin/env python

from wtforms import Form, BooleanField
from wtforms import TextField, SubmitField, IntegerField
from wtforms.validators import Length, required, DataRequired


class SetInfoForm(Form):
    company_id = IntegerField('Company', [required()])
    company_name = TextField('Company', [Length(max=255), required()])
    sprint_id = IntegerField('Sprint', [required()])
    sprint_name = TextField('Sprint Name', [Length(max=255)])
    submit = SubmitField("Send")

# if__name__ == '__main__':
