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

   
##### 07/13/2016
   - reconstruct the project
      * update the database

   - stanfor parser
      *  using the python wrapper in NLTK for it


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

   - using the Stanford lib in NLTK or the third python wrapper? 

   - coding 

##### 07/15/2016
   - the stanford parser dir:
   /Users/zhaowenlong/workspace/lib/nltk_data/jars  

   - coding/debugging the conj part
      -

##### 07/16/2016
   -  coding the code about advcl 
     >"Since/Because he came, I left." --> "He came.  Therefore I left." 

##### 07/19/2016
   - 早睡早起 
   - wordnet + Roget's thesaurus 
   -

##### 07/25/2016
   -  how to know the adverbial clauses
   -  动词时态

##### 08/08/2016
   - flask with CKEditor for the inline editing

##### 08/10/2016
   * about the word
     - pos
     - add the hyponym

   * pyvenv-workon  

###### 09/02/2016
   * C1, C2 -> C11+ C12
     - 是否来源于相同的父亲


##### Next

##### 11/22/2016


##### 02/17/2017

## the interface

[checkbox] Simplify the vocabulary
[checkbox] Simplify sentence structures

If "Simplify the vocabulary" is checked, show:
[radio button] Use default vocabulary list
[radio button] Customize vocabulary list

If "Simplify sentence structures" is checked, show:
[radio button] Simplify all complex structures
[radio button] Simplify selected structures only

- done

## the syntactic part improvement in mturk 

  - prepositiocnal phrease post-modification

  - adjectivl post-modification

### 01/03
 about the website
  - one is about keeping the updated setting, another one is about the font size
  - 

 about the paper
   - "an architecture for a text simplification system"

  - 

### preparation
  - trustworthy - the information
  - don't complain about your boss
  - treat your boss with respect
  - try to make your boss look good
  - make a list of what you plan to do in the next week
  - briefly tell him what the problem is and then offer up a couple of solutions

  - defer to the boss
     This is what we're planning to talk about today.
     is there something else that you actually feel is more urgent for us to talk about?
  - don't be afraid to ask for help

  - periodically make sure you let her know about your accomplishments and any great feedback you’ve received.
  
  - ask your boss for honest feedback
    > find out what the issues are,


### the talk
  - Could you possibly have some time now ?

  - Could I possibly be a research student here? I wanna be a researcher
    Is it all right I should submit the application online and wait for the message?

  - Could you possibly be my supervisor ?

  - Could I have a meeting time regularly?

#### the system
  - the checkbox button
  - hide the 'disable' one in the 'the vocabulary' choice
  - give the output of the 'bold' words
    > print(wn.synset('dog.n.01').definition())

#### super sense Tagging task ->  a classification problem
   - SemEval-2016 Task 10: 
      http://alt.qcri.org/semeval2016/task10/
      http://dimsum16.github.io/

   - http://medialab.di.unipi.it/evalita2011/
     - 2013: Evalita 2011: Description and Results of the SuperSense Tagging Task
   - 2001 - Supervised sense tagging using support vector machines
   - 2013 - Super-Sense Tagging Using Support Vector Machines and Distributional Features
   - 2013 - SuperSense Tagging with a Maximum Entropy Markov Model

   - 2016: Supersense tagging with inter-annotator disagreement
   - 2016: WHUNlp at SemEval-2016 Task DiMSUM: A Pilot Study in Detecting Minimal Semantic Units and their Meanings using Supervised Models
   - 2016: UTU at SemEval-2016 Task 10: Binary Classification for Expression Detection (BCED)
   - 2016: A Corpus of Preposition Supersenses in English Web Reviews
   - 2016: The Preposition Corpus in the Sketch Engine
   - 2016: Supersense Embeddings: A Unified Model for Supersense Interpretation, Prediction, and Utilization
    
   - ICL-HD at SemEval-2016 Task 10: Improving the Detection of Minimal Semantic Units and their Meanings with an Ontology and Word Embeddings

   - Supersense tagging for Danish
   - A Resource and Tool for Super-sense Tagging of Italian Texts
   - Simple task-specific bilingual word embeddings∗
   - A Survey of WordNet Annotated Corpora


#### 03/20/2017
   
   issues
   - click the two choices by default
     - the issue
   - split the two choices

####
  - unclick the two choices, the system gives the error
  - split the two functions

#### 03/27/2017
  - test the issues, and merge it into the code on the server 5001
  -  merge the code to 5000
  - notice Dr.

#### 04/07/2018
  "Peter arrived, bringing a gift."
   - remember the checkbox selections
   - 

  super-sense : annotate each word with a general/abstract concept

   wordnet supersense ares top-level
   Using the WordNet lexicographer classes -> information at the synset level   
  the set of meanings for each word is provided by a wordNet super-senses
    : lemma, pos tags, 

#### 04/23/2017
  * make supersense tagger work locally
  * TODO: the input and output format of the AMALGrAM

#### 05/29/2017
  * Peter ate fish and drank water.
  
  For syntactic simplification:
- A sentence that has two of the constructs (e.g., relative clause and coordination); show the different output sentences when one or both of the constructs are de-selected;
  > example: "Peter, who attended the conference, delivered a speech and met new researchers."
  [done]: the 'merge' button is lost, and the reason is that check_word function (u'researchers.'-> u'researchers', '.'')
    - [bugs] (if the user only keeps the choice, it works)
    - [done]

  >>> hide the wordlist when the choice is given
  >>> the 'merge' button
  >>> hide the alg choices
  >>> the 

  >>> just keep the name, not pronoun
  >>> when lexical choice is changed, it doesnot work
  >>> the word list selections ----- 
  >>> after the user reselect the algs, it doesnot work

- A sentence that has an organization/male/female name; show how the pronoun in the second sentence is generated.
  [talked with Buddhika]
   >Peter, my friend, bought an automobile.
   >Alicia, my friend, bought an automobile.
   >London, the capital of England , is a city with high population.

- A sentence that is split three times (i.e. into four output sentences).  Show how to use the merge function to roll back the splits.
   >Because he insisted and she invited, Peter attended the seminar and delivered a speech.
    - [bugs](the reason is the same as the 1st one)

  For lexical simplification:
- A sentence that has two words at two different HK vocab levels that can be simplified; show the different output sentences when different vocab levels are selected;
  > The event was a catastrophe.

- Choose a word with two different meanings.  Choose two sentences so that different definitions would be shown for this word.
  > He eats an apple .
  > He bought an apple computer .

- A sentence in which a two-word sequence can be simplified (you might need to ask Lis).
  > Hong Kong has a legislative system.


#### 05/29/2017





- "London, the capital of England , is a city with high population."
No “it” for London
   [lis will check this]


- A sentence that is split three times (i.e. into four output sentences).  Show how to use the merge 
function to roll back the splits.
  > Because he insisted and she invited, Peter attended the seminar and delivered a speech."
  - done

  > The event was a catastrophe.
- "catastrophe" was simplified (to "tragedy") at Secondary 6 but not in Primary 3
  - The result is right.
  The reason is that the candidate of the word should also be in the selected level.
  For example, 
  The word 'catastrophe' has the following candidates: [u'catastrophe', u'disaster', u'tragedy'],
  The candidates 'disaster' and 'tragedy' are not inclued in Primary 6, so the system only show the difficult word itslef.

  While in Secondary 3, which included the word 'tragedy' ('disaster' is not in the level), this means that there is the drop-down:  [u'catastrophe', u'tragedy']

  Secondary 6 level includes the word 'catastrophe', the system doesnot give the drop-down list.



- "Peter, my friend, bought an automobile."
There should be a drop down list for Peter in second sentence
There should not be a drop down list for Peter after merging

  [fixed]

- After de-selecting and selecting syntactic simplification, the system doesn’t run.
   [fixed]
  > "Peter, my friend, bought an automobile."

- Hide vocab list field unless second option is chosen.
  > when the 1st choice is selected, the vocab list should be hidden

- Hide list of construct unless second option is chosen.

- Do not hide vocab list after changing "Secondary 6" to "Secondary 3"

  > remember the user's choice after the refresh

##### reference
 - Natural Language Processing With Python
 - flask framework
 - stanford NLP course
 