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
Bacterial contaminants are ubiquitous , and foods left unused too long will often acquire substantial amounts of bacterial colonies and become dangerous to eat , leading to food poisoning . 

bacterial contaminants are ubiquitous.  foods left unused too long will often acquire substantial amounts of bacterial colonies.  they become dangerous to eat.  they lead to food poisoning .  

Bacterial contaminants are ubiquitous  .  foods left unused too long will often acquire substantial amounts of bacterial colonies and become dangerous to eat , leading to food poisoning . Bacterial contaminants are ubiquitous  .  

foods left unused too long will often acquire substantial amounts of bacterial colonies and become dangerous to eat , leading to food poisoning . 

 coordi@@                    

###### ex2
Cobra and Tango and Cash did solid business domestically but overseas they did blockbuster business grossing over $ 100 million in foreign markets and over $ 160 million worldwide . 

cobra and tango and cash did solid business domestically.  but overseas they did blockbuster business.  they grossed over $ 100 million in foreign markets and over $ 160 million worldwide.  

Cobra and Tango and Cash did solid business domestically .  they did blockbuster business grossing over $ 100 million in foreign markets and over $ 160 million worldwide . 

Cobra and Tango and Cash did solid business domestically .  they did blockbuster business grossing over $ 100 million in foreign markets and over $ 160 million worldwide . 

['N'] coordi@@               

##### ex3

At present it is formed by the Aa , which descends from the Rigi and enters the southern extremity of the lake .  at present it is formed by the aa.  it descends from the rigi and enters the southern extremity of the lake.  At presented it is formed by the Aa  .   it descends from the Rigi .   it  enters the southern extremity of the lake .  At presented it is formed by the Aa . it descends from the Rigi and enters the southern extremity of the lake . ['N'] adverb@@coordi                         
##### ex4
Notrium is played from a top-down perspective , giving an overhead view of proceedings .  "notrium is played from a top-down perspective.  it gives an overhead view of proceedings.
" Notrium is played from a top-down perspective . It gave an overhead view of proceedings . . Notrium is played from a top-down perspective . It gave an overhead view of proceedings . . ['N'] adverb@@                    

##### EX5
Fired by enthusiasm , Tolstoy returned to Yasnaya Polyana and founded thirteen schools for his serfs ' children , based on ground-breaking libertarian principles Tolstoy described in his 1862 essay `` The School at Yasnaya Polyana '' . tolstoy was fired by enthusiasm. he returned to yasnaya polyana.  he founded thirteen schools for his serfs ' children.  they were based on ground-breaking libertarian principles.  tolstoy described them in his 1862 essay `` the school at yasnaya polyana '' . Tolstoy was fired by enthusiasm  .  He returned to Yasnaya Polyana and founded thirteen schools for his serfs ' children . He based on ground-breaking libertarian principled Tolstoy described in his 1862 essay `` The School at Yasnaya Polyana '' . Tolstoy was fired by enthusiasm . He returned to Yasnaya Polyana and founded thirteen schools for his serfs ' children , based on ground-breaking libertarian principles Tolstoy described in his 1862 essay `` The School at Yasnaya Polyana '' .  ['N'] adverb@@adverb                    

##### ex6
Jamie Farr is an American television and film actor and popular game show panelist .  jamie farr is an american television.  he is also film actor.  he is also a popular game show panelist. Jamie Farr is an American television  .   He is film actor . He is popular game show panelist . Jamie Farr is an American television . He is film actor and popular game show panelist .  ['N'] coordi@@coordi    


##### ex7
While each edition of Windows 2000 was targeted to a different market , they share a core set of features , including many system utilities such as the Microsoft Management Console and standard system administration applications .  each edition of windows 2000 was targeted to a different market.  but they share a core set of features.  they include many system utilities such as the microsoft management console and standard system administration applications.  Each edition of Windows 2000 was targeted to a different market  . But they share a core set of features , including many system utilities such as the Microsoft Management Console and standard system administration applications . Each edition of Windows 2000 was targeted to a different market  . But they share a core set of features , including many system utilities such as the Microsoft Management Console and standard system administration applications . ['N'] subordi@@                                   

#### questions
* the database

* AJAX with jQuery in Flask ?

* Python loading dir?



 
  