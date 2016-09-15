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
 *  Peter is studying at Stony Brook University .

  The companies -> not "organization"

 *  She is a teacher serving as a volunteer .







#### questions
* the database

* AJAX with jQuery in Flask ?

* Python loading dir?



 
  