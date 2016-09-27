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
    wordinput = TextField("wordinput")
    wordlevel = SelectField('The level', choices = [(0, 'level 0'), (1, 'level 1'), (2, 'level 2'), (3, 'level 3'), (4, 'level 4')])
    submit = SubmitField('Submit')

# The function is used in setting
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class SelectForm(Form):
    #wordinput = TextField("wordinput")
    #wordlist = RadioField('The wordlist', choices= [('0','The Level')])
    #wordlevel = SelectField('The level', choices = [(1, 'level 1'), (2, 'level 2'), (3, 'level 3'), (4, 'level 4')])
    algs = MultiCheckboxField('The Types', choices = [(1,'Coordination'), 
    	                                       (2,'Subordination'), 
    	                                       (3,'Adverbial clauses'), 
    	                                       (4,'Participial phrases'), 
    	                                       (5,'Relative clauses'), 
    	                                       (6,'Appositive phrases'), 
    	                                       (7,'Passive voice')])

    submit =SubmitField("Submit")
