# -*- coding: utf-8 -*-
"""
  The Login form
  The Entry Form
  The 
  TODO: the registration form

@author wenlong
"""
from flask_wtf import Form
from wtforms import TextField, IntegerField, SubmitField, SelectField, SelectMultipleField, widgets, validators, ValidationError

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

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class SelectForm(Form):
    words = TextField("words")
    edblist = SelectField('EDBlist', choices = [(1, 'list1'), (2, 'list2'), (3, 'list3'), (4, 'list4')])
    algs = MultiCheckboxField('Algorithm', choices = [(1,'punct'), 
    	                                       (2,'coordi'), 
    	                                       (3,'subordi'), 
    	                                       (4,'adverb'), 
    	                                       (5,'parti'), 
    	                                       (6,'adjec'), 
    	                                       (7,'appos'), 
    	                                       (8,'passive'), 
    	                                       (9,'paratax')])

    submit =SubmitField("Send")
