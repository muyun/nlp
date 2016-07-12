##### notes about NLP
 - 

##### About Flask
* notes about Flask

* running   
   To enable debug mode so that the the server will reload itself on code changes   
     >export FLASK_DEBUG=1  
     
   cmd:   
     >export FLASK_APP=simptext   
     >python -m flask initdb  
     >python -m flask run  

* using virtual Environments to separate the development and maintance 
    >virtualenv --no-site-packages venv 
    > . venv/bin/activate 
    >deactivate 
    
    “freeze” the current state of the environment packages  
    > pip freeze > requirements.txt 
    > pip install -r requirements.txt 
   

* TODO:
  * being module for the flexible and scalable


#### reference
* [The Hitchhiker’s Guide to Python](http://docs.python-guide.org/en/latest/)
* [thinkpython2](http://www.greenteapress.com/thinkpython2/html/index.html)
* [python alg](http://www.brpreiss.com/books/opus7/html/book.html)
* [celery](http://celery.readthedocs.io/en/latest/index.html)
* 
* [Natural language understanding (almost) from scratch](https://blog.acolyer.org/2016/07/04/natural-language-understanding-almost-from-scratch/)
* [NLP](https://www.eecis.udel.edu/~trnka/CISC889-11S/)
