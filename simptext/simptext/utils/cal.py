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


def get_lemma(word):
    return wnl.lemmatize(word.lower(), pos='v')

def check_word(strs, words):
    """ check the word is words list, and return the string"""
    #output=[]
    #output= OrderedDict()
    print "strs: ", strs

    #import pdb; pdb.set_trace()
    #for w in str(strs).split():
    tokens = StanfordTokenizer().tokenize(strs)
    for ind in range(len(tokens)):
        #print 'token: ', token
        if tokens[ind] in string.punctuation:
            #print "stro :", token
            #output[token] = token
            pass
        else:
            #_w = w.lower()
            # so slow here
            #_token_ = StanfordTokenizer().lemmatize(token.lower())
            #_token = wnl.lemmatize(token.lower(), pos='v')
            _token = get_lemma(tokens[ind])
            
            #print "token: ", token

            if _token in words:
                 #output[token] = token
                 pass
            else:
                 tokens_dict = {}
                 _output = []
                 _output.append(tokens[ind]) # put the word itself at first

                 wordnet_list = get_wordnet_list(_token)
                 for _w in wordnet_list:
                     if _w in words: # w in EDB list?
                         _output.append(_w)

                 if len(_output) >= (1+1): # there is a replace including the word iteself
                     tokens_dict[tokens[ind]] = _output
                     tokens[ind] = tokens_dict
                 else:
                     pass
                     
    #import pdb; pdb.set_trace()
    #return ' '.join(str(w) for w in output)
    return tokens


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
