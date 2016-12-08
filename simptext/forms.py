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

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class LoginForm(Form):
    username=TextField('username', [validators.Length(min=4, max=25)])
    #password= PasswordField('password',[validators.DataRequired()])
    submit = SubmitField('Submit')

AVAILABLE_CHOICES = [ (1,'Subordination (e.g. "Since he was late, I left.")'),
                      (2,'Adverbial Clauses (e.g. "Impatient, he stood up.")'),
                      (3,'Appositive phrases (e.g. "Peter, my friend, ate an apple.")'), 
                      (4,'Coordination (e.g. "I ate an apple and he ate an orange.")'),
                      (5,'Participial phrases (e.g. "Peter, running down the street, tripped.")'),
                      (6,'Relative clauses (e.g. "Peter, who liked fruits, ate an apple")'),
                      (7,'Passive voice (e.g. "An apple was eaten by Peter.")')]

                                         
# The function is replaced by database
class EntryForm(Form):
    text=TextField('input', [validators.Length(min=4, max=25)])
    #words=StringField('password', [validators.Length(min=4, max=25)])
    #password= PasswordField('password',[validators.DataRequired()])
    wordinput = TextField('wordinput')
    wordlevel = SelectField('The level:', choices = [(0, 'custom'), (1, 'level 1'), (2, 'level 2'), (3, 'level 3'), (4, 'level 4')])
    algs = MultiCheckboxField('The simplification procedures:', 
                                 choices = AVAILABLE_CHOICES, default=[1,2,3,4,5,6,7,8,9])

    submit =SubmitField("Submit")


# The function is used in setting
class SelectForm(Form):
    wordinput = TextField("wordinput")
    wordlevel = SelectField('The level:', choices = [(0, 'custom'), (1, 'level 1'), (2, 'level 2'), (3, 'level 3'), (4, 'level 4')], default=4)
    algs = MultiCheckboxField('The simplification procedures:', 
                                 choices = AVAILABLE_CHOICES, default=[1,2,3,4,5,6,7,8,9])
    #submit =SubmitField("Submit")
