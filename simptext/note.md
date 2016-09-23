####  NOTE

#### The installaton note
* virtualenvwrapper is used for the virtual env management  
> $ export WORKON_HOME = $HOME/.virtualenvs  
  $ source /usr/local/bin/virtualenvwrapper.sh  
  $   
  $ mkvirtualenv venv2 ## create   
  $ workon venv2 #working   
  $ (Emacs) M-x pyvenv-workon venv2   
  $   
  $ deactivate   
  $ rmvirtualenv venv2   

* “freeze” the current state of the environment packages   
> $ pip freeze > requirements.txt   
  $ pip install -r requirements.txt   

* About the sqlalcemy  
> $ from app import db  
  $ db.create_all()  
  $ import model  
  $ txt = model.Entry('this is a demo')  
  $ db.session.add(txt)  
  $ db.session.commit() 


#### example 
 *  Peter, my friend, ate an apple .


#### install
pip install openpyxl --upgrade

zhaowenlong@zhaowenlongs-MacBook:~/workspace/proj/dev.nlp/simptext/simptext$ python evaluate.py
#num_negative:  262
#num_false_positive:  0
#num_true_positive:  32
#num_false_negative:  186
#num_true_negative:  76
#num_positive:  32
#_num_output:  294

zhaowenlong@zhaowenlongs-MacBook:~/workspace/proj/dev.nlp/simptext/simptext$ python evaluate.py
#num_negative:  284
#num_false_positive:  0
#num_true_positive:  10
#num_false_negative:  208
#num_true_negative:  76
#num_positive:  10
#_num_output:  294


#### questions
* the database

* AJAX with jQuery in Flask ?

* Python loading dir?



 
  