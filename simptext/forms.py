# -*- coding: utf-8 -*-
"""
  The Login form
  The Entry Form
  The setting Form
  TODO: the registration form

@author wenlong
"""
from flask_wtf import Form
from wtforms import TextField, IntegerField, SubmitField, RadioField, SelectField, SelectMultipleField, widgets, validators, ValidationError

class LoginForm(Form):
    username=TextField('username', [validators.Length(min=4, max=25)])
    #password= PasswordField('password',[validators.DataRequired()])
    submit = SubmitField('Submit')


# The function is replaced by database
class EntryForm(Form):
    text=TextField('input', [validators.Length(min=4, max=25)])
    #words=StringField('password', [validators.Length(min=4, max=25)])
    #password= PasswordField('password',[validators.DataRequired()])
    submit = SubmitField('Submit')

# The function is used in setting
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class SelectForm(Form):
    wordinput = TextField("wordinput")
    #wordlist = RadioField('The wordlist', choices= [('0','The Level')])
    wordlevel = SelectField('The level', choices = [(1, 'level 1'), (2, 'level 2'), (3, 'level 3'), (4, 'level 4')])
    algs = MultiCheckboxField('The Algorithm', choices = [(1,'punct'), 
    	                                       (2,'coordi'), 
    	                                       (3,'subordi'), 
    	                                       (4,'adverb'), 
    	                                       (5,'parti'), 
    	                                       (6,'adjec'), 
    	                                       (7,'appos'), 
    	                                       (8,'passive'), 
    	                                       (9,'paratax')])

    submit =SubmitField("Submit")
