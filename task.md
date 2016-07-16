#### todo list

##### 16/06/2016
Would you please come to my office (AC1-B7706) at 2pm?

implement a web interface that 
(1) lets the user type/paste an English text; 
(3) lets the user edit the simplified text and export it.
  -- django
  - use flask to replace diango

(2) automatically simplifies the text
  -- word substitution , and sentence structure simplification
  -- sentence analysis

   Stanford dependencies 
   
  a directed graph representation, in which words in
the sentence are nodes in the graph and grammatical relations are edge labels.

##### 17/06/2016
 - use the Flask framework

 - you shouldn't get up at noon
 - take care your sayings now, be nice, hard-working and patient

##### 20/06/2016
 - let the blog running

##### 21/06/2016
 - modify the blog to meet the requirement

   e.g., "The ceremony commences in one hour." --> "The ceremony starts in one hour.") and sentence structure simplification (e.g., "He likes apples but hates oranges." --> "He likes apples.  But he hates oranges.") 

  WordNet

##### 22/06/2016
 - print the output in html
 -

##### 23/06/2016
 - Ajax with jQuery for the dynamic editing function

   issue: 
     1.  the "wordlist.xlsx" cannot give the full word list

    doing:
     2.  Ajax is to create fast and dynamic web pages

     3.  WordNet and nltk interface -> - PyWordNet


##### 24/06/2016
  - add the Drop-down list of choices with multiple selection
     * The Flask-WTF extension is so flexible and scalable
     
     * TODO: Ajax with jQuery is better

##### 25/06/2016
  - The wordnet function 
  - some doc on Python

  - Stanford Parser ...

#####  26/06/2016
  - some doc on Flask

#####  27/06/2016
  - Make the browser interface look better
    * being module might be better, and be more flexible, scalable

  - Stanford parser ...
    * the low NLTK version -> should be the latest one
    * THE global variables setup issue

 -  Some doc 
  
##### 28/06/2016
  - Stanford parser ...
    * The CLASSPATH SETUP problem
    * java version 
    * ...

  - having the TEST/DEBUG module might be better

##### 29/06/2016
  - should be earlier, and be nice

  - current one requires Java 1.8+
     and should setup the CLASSPATH variable

     issue: read the mannual for the sentence

  - wordnet version : 3.0
     ~/nltk_data/corpora/wordnet_ic/README

  - add the lemma function

  - read the coinco doc


##### 30/06/2016
  - read the coinco README
  - Using lib for the parser
    + the 'Beautiful Soup' lib doc
    + lxml installation

  - coding   

##### 04/07/2016
  - coding/debugging the functions

  - some results:
    #sentences:  2474
    #words:  42792
    #words marked with synonyms:  15629

    #words in the EDB list:  1222
    #words not in the EDB list:  3922


   - check the serialization/de ?  


##### 05/07/2016
   - TODO-stanford dependency parser
   - using JSON format 
   
   - fix the errors in Flask
   - some doc about python/flask  
   
   - code the part about intermediate value output

##### 06/07/2016
   - optimize the code module

##### 07/07/2016 
   - optimize the code
    
   - update the code for the updated dataset

   - SemEval-2007
     * Only use trial dataset lex- sub trial.xml now(not including test dataset)

     * The data set comprises 2010 sentences (201 target words each with 10 sentences)?


##### 07/08/2016
   - Mechanical Turk dataset
    * aligning Simple English Wikipedia and English Wikipedia.
    * 137K aligned sentences pairs ?
   
   - read the doc

  - read Roget's Thesaurus doc

##### 07/10/2016
   - Use the original 1911 Roget's Thesaurus (1911) now
      * an edition updated with 2200 words (called "1911X1") and an edition updated with 5500 words (called "1911X5")
      * a script to transfer xml to txt?

      * use the Roget's Thesaurus Electronic Lexical Knowledge Base (ELKB)

      cross-references ...
   
  - part-of-speech: syntactic role

##### 07/11/2016
   - for roget l1

   - TODO: 
      * update the code for POS
      * check sem
      * setence split

##### 07/12/2016
   - reconstruct the system
     * use the virtual Environments to split the working and maintaining project
     *  being a bit more system

   - stanfor parser
      *  using the python wrapper in NLTK for it

##### 07/13/2016
   - reconstruct the system


##### 07/14/2016
   - Stanford parser
     dependency_tag(governor, dependent) 

     >tokens
       StanfordSegmenter -> for chinese
       StanfordTokenizer -> for english

     > Named Entity Recognizer
     StanfordNERTagger

     > 词性标注
     StanfordPOSTagger

     > Syntactic analysis
     StanfordParser

     StanfordDependencyParser

     StanfordNeuralDependencyParser  

##### 07/15/2016
   - the stanford parser dir:
   /Users/zhaowenlong/workspace/lib/nltk_data/jars  

   - using the Stanford lib in NLTK or the third python wrapper? 

##### reference
 - Natural Language Processing With Python
 - flask framework
 - stanford NLP course
 