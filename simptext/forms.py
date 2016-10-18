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


# The function is replaced by database
class EntryForm(Form):
    text=TextField('input', [validators.Length(min=4, max=25)])
    #words=StringField('password', [validators.Length(min=4, max=25)])
    #password= PasswordField('password',[validators.DataRequired()])
    wordinput = TextField("wordinput")
    wordlevel = SelectField('The level:', choices = [(0, 'level 0'), (1, 'level 1'), (2, 'level 2'), (3, 'level 3'), (4, 'level 4')], default=4)
    algs = MultiCheckboxField('The simplification procedures:', choices = [(1,'Punctuation'), 
                                             (2, 'Coordination'),
                                             (3,'Subordinated Clauses'),
                                             (4,'Adverbial Clauses'), 
                                             (5,'Participial phrases'),
                                             (6,'Adjectival Clauses'),
                                             (7,'Appositive phrases'), 
                                             (8,'Passive voice'),
                                             (9,'Parataxis')], default=[1,2,3,4,5,6,7,8,9])


    submit = SubmitField('Submit')


# The function is used in setting
class SelectForm(Form):
    #wordinput = TextField("wordinput")
    wordinput = TextField("wordinput")
    wordlevel = SelectField('The level', choices = [(0, 'level 0'), (1, 'level 1'), (2, 'level 2'), (3, 'level 3'), (4, 'level 4')], default=4)
    algs = MultiCheckboxField('The types', choices = [(1,'Coordination'), 
    	                                       (2,'Subordination'), 
    	                                       (3,'Adverbial clauses'), 
    	                                       (4,'Participial phrases'), 
    	                                       (5,'Relative clauses'), 
    	                                       (6,'Appositive phrases'), 
    	                                       (7,'Passive voice')])

    submit =SubmitField("Submit")
