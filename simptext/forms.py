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

AVAILABLE_CHOICES_ = [ (1,'Subordination (e.g. "Since he was late, I left.")'),
                      (2,'Adverbial Clauses (e.g. "Impatient, he stood up.")'),
                      (3,'Appositive phrases (e.g. "Peter, my friend, ate an apple.")'),
                      (4,'Coordination (e.g. "I ate an apple and he ate an orange.")'),
                      (5,'Participial phrases (e.g. "Peter, running down the street, tripped.")'),
                      (6,'Relative clauses (e.g. "Peter, who liked fruits, ate an apple")'),
                      (7,'Passive voice (e.g. "An apple was eaten by Peter.")')]

AVAILABLE_CHOICES = [ (1,'Parataxis </br> <small> e.g. "Peter - nobody guessed it - showed up." --> "Peter showed up. Nobody guessed it." </small>'),
                      (2,'Punctuation  </br> <small> e.g. "I ate fish; he drank water." --> "I ate fish. He drank water."</small>'),
                      (3,'Adjectival Clauses </br> <small> e.g. "The automobile, which Peter bought, was scarlet." --> "Peter bought the automobile. The automobile was scarlet."</small>'),
                      (4,'Subordination </br> <small> e.g. "Since he was late, I left." --> "He was late. So, I left ."</small>'),
                      (5,'Appositive phrases </br> <small>  e.g. "Peter, my friend, bought an automobile." --> "Peter was my friend. Peter bought an automobile."</small>'),
                      (6,'Adverbial Clauses </br> <small> e.g. "Impatient, he stood up." --> "He was impatient. He stood up."</small>'),
                      (7,'Coordination </br> <small> e.g. "Peter ate fish and drank water." --> "Peter ate fish. Peter drank water."</small>'),
                      (8,'Participial phrases </br>  <small> e.g. "Alicia, running down the street, tripped." --> "Alicia was running down the street. Alicia tripped."</small>'),
                      (9,'Relative clauses </br>  <small> e.g. "Peter, who liked fruits, ate an orange." --> "Peter ate an orange. Peter liked fruits."</small>'),
                      (10,'Passive voice </br>  <small> e.g. "The design was tailored by Peter. --> "Peter tailored the design."</small>')]

                                         
# The function is replaced by database
class EntryForm(Form):
    text=TextField('input', [validators.Length(min=4, max=25)])
    #words=StringField('password', [validators.Length(min=4, max=25)])
    #password= PasswordField('password',[validators.DataRequired()])
    wordinput = TextField('wordinput')
    cselect = MultiCheckboxField('The choices:', choices = [(1, '1'), (2, '2')], default=[1,2])
    wordlevel = SelectField('The level:', choices = [(0, 'custom'), (1, 'level 1'), (2, 'level 2'), (3, 'level 3'), (4, 'level 4')], default=4)
    algs = MultiCheckboxField('The simplification procedures:', 
                                 choices = AVAILABLE_CHOICES, default=[1,2,3,4,5,6,7,8,9,10])

    submit =SubmitField("Submit")


# The function is used in setting
class ParamForm(Form):
    wordinput = TextField("wordinput")
    cselect = MultiCheckboxField('The choices:', choices = [(1, '1'), (2, '2')], default=[1,2])
    wordlevel = SelectField('The level:', choices = [(0, 'custom'), (1, 'level 1'), (2, 'level 2'), (3, 'level 3'), (4, 'level 4')], default=4)
    algs = MultiCheckboxField('The simplification procedures:', 
                                 choices = AVAILABLE_CHOICES, default=[1,2,3,4,5,6,7,8,9,10])
    #submit =SubmitField("Submit")    
