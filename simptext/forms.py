# -*- coding: utf-8 -*-
"""
  the login form
  TODO: the registration form

@author wenlong
"""

from wtforms import Form, StringField, SubmitField, PasswordField, validators

class LoginForm(Form):
    username=StringField('username', [validators.Length(min=4, max=25)])
    #password= PasswordField('password',[validators.DataRequired()])
    submit = SubmitField('Submit')


class EntryForm(Form):
    text=StringField('username', [validators.Length(min=4, max=25)])
    #password= PasswordField('password',[validators.DataRequired()])
    submit = SubmitField('Submit')