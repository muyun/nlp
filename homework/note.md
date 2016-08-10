##### note about Flask
* Use virtual Environments to separate the development from the maintance 
    - virtualenvwrapper is used for the virtual env management
      > $ export WORKON_HOME = $HOME/.virtualenvs  
        $ source /usr/local/bin/virtualenvwrapper.sh   
        $     
        $ mkvirtualenv venv2  ## create   
        $ workon venv2 
        $ (Emacs) M-x pyvenv-workon venv2   
        $    
        $ deactivate  
        $ rmvirtualenv venv2

    - “freeze” the current state of the environment packages  
      > pip freeze > requirements.txt   
      > pip install -r requirements.txt 

* Structuring
 - module

* unicode 
   - text is encoded (An encoding is a set of rules that assign numeric values to each text character)  
   - UTF-8 is an extension of ASCII  

   - s.decode(encoding) -> str-> unicode  
     u.encode(encoding) -> unicode -> str  

   - unique is a way to represent text without bytes  
    unicode is a concept, to save unicode to disk you have to encode it

   - The default python2 encoding is ASCII  
      sys.setdefaultencoding('utf-8')  

    - python2 unicode incompatibility - csv module   

    - decode early, unicode everywhere, encode late


   
##### note about NLP
  * Part-of-speech (POS) tagging  
    Chunking -> labels phrases or segments with tags  
    Named-entity recognition (NER) -> labels recognised entities  
    Semantic-role labeling (SRL)  

  * hand-engineered features -> assign label to words  