# -*- coding: utf-8 -*-
"""
   utils.cal
   ~~~~~~~~~~
   calculation

@author wenlong
"""

from collections import OrderedDict

#import nltk
from nltk.corpus import wordnet as wn

#Use StanfordTokenizer
from nltk.tokenize import StanfordTokenizer
#from nltk.tokenize import wordpunct_tokenize

# lemma

from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()

import string

import dt

def check_word(strs, words):
    """ check the word is words list, and return the string"""
    #output={}
    output= OrderedDict()
    print "strs: ", strs

    #import pdb; pdb.set_trace()
    #for w in str(strs).split():
    for token in StanfordTokenizer().tokenize(strs):
        #print 'token: ', token
        if token in string.punctuation:
            #print "stro :", token
            output[token] = token
        else:
            #_w = w.lower()
            # so slow here
            #_token_ = StanfordTokenizer().lemmatize(token.lower())
            _token = wnl.lemmatize(token.lower(), pos='v')
            
            print "token: ", token

            if _token in words:
                 output[token] = token
            else:
                 output[token] = get_wordnet_list(_token)

    #import pdb; pdb.set_trace()
    #return ' '.join(str(w) for w in output)
    return output


def lemma_words(words):
    output=[]
    for w in words:
        _w = wnl.lemmatize(w.lower(), pos='v')
        

def get_wordnet_list(w):
    """ replace the words, using the synonyms  """
    #TODO: should limit the lemma number
    wordnet=[]
    for synset in wn.synsets(w):  # get the synonyms
        for lemma in synset.lemmas():
            #print lemma.name()
            wordnet.append(lemma.name())

    return list(set(wordnet)) 

"""
def cal_stat_info(filename):
    #filename="/Users/zhaowenlong/workspace/proj/dev.nlp/web/simptext/dataset/coinco/coinco_172.xml"

    lemmas = {}
    #import pdb; pdb.set_trace()
    [num_sentences, num_words, num_words_syn, lemmas] = get_stat_info(filename)

    return
"""
