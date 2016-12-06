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

AVAILABLE_CHOICES = [ (1, 'Parataxis (e.g. "Peter - nobody guessed it - showed up.")'),
                                             (2,'Subordinated Clauses (e.g. "Before he came, I left.")'),
                                             (3,'Adverbial Clauses (e.g. "Needing money, I begged my parents.")'), 
                                             (4,'Participial phrases (e.g. "Alicia, running down the street, tripped.")'),
                                             (5,'Adjectival Clauses (e.g. "The apple, which Peter ate, was red.")'),
                                             (6,'Appositive phrases (e.g. "Peter, my son, ate an apple.")'), 
                                             (7,'Passive voice (e.g. "Peter was hit by a bus.")' ),
                                             (8,'Punctuation (e.g. "I ate fish; he drank wine.")'),
                                             (9, 'Coordination (e.g. "Peter ate fish and drank wine.")')]

                                         
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
    wordlevel = SelectField('The level:', choices = [(0, 'level 0'), (1, 'level 1'), (2, 'level 2'), (3, 'level 3'), (4, 'level 4')], default=4)
    algs = MultiCheckboxField('The simplification procedures:', 
                                 choices = [ (1,'Punctuation (e.g. "I ate fish; he drank wine.")'), 
                                             (2,'Subordinated Clauses (e.g. "Before he came, I left.")'),
                                             (3,'Adverbial Clauses (e.g. "Needing money, I begged my parents.")'), 
                                             (4,'Participial phrases (e.g. "Alicia, running down the street, tripped.")'),
                                             (5,'Adjectival Clauses (e.g. "The apple, which Peter ate, was red.")'),
                                             (6,'Appositive phrases (e.g. "Peter, my son, ate an apple.")'), 
                                             (7,'Passive voice (e.g. "Peter was hit by a bus.")' ),
                                             (8,'Parataxis (e.g. "Peter - nobody guessed it - showed up.")'),
                                             (9, 'Coordination (e.g. "Peter ate fish and drank wine.")')])
    submit =SubmitField("Submit")
