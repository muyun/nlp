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



     Use the dataset:


http://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/coinco.html

Some words in this dataset have synonyms, say: X --> {A, B, C}, Y --> {P, Q}


Look up the synonym list from WordNet, say: X --> {B, D, E}, Y --> {R, S}


We can now calculate the maximum possible performance ("ceiling") of our simplification algorithm.  If the two lists have at least one common word ("B" for X), then it would be possible for the algorithm to return the correct answer.  If the two lists do not overlap (for Y), then it is impossible for the algorithm to return the correct answer.


Please calculate the "ceiling" for all words that are *not* in the Education Bureau list. 
 
##### reference
 - Natural Language Processing With Python
 - flask framework
 - stanford NLP course
 