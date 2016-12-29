#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  simptext.wordcal
  ~~~~~~~~~~~~~~~~~
  The words processing

@author: wenlong
"""

from collections import OrderedDict

import nltk
from nltk.corpus import wordnet as wn

#Use StanfordTokenizer
#from nltk.tokenize import StanfordTokenizer
from nltk.tokenize import wordpunct_tokenize
from nltk.tokenize import StanfordTokenizer
from nltk.tag import StanfordPOSTagger
st = StanfordPOSTagger('english-bidirectional-distsim.tagger')

# lemma
from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()

import string

#import sys
#sys.setrecursionlimit(1000)

# the Models about the training model about the word rank
from models import rank

def get_word_pos(w):
    "return the word@pos from NLTK"
    pos = nltk.tag.pos_tag([w])[0][1]

    #import pdb; pdb.set_trace()
    return w+"@"+pos

def _get_hyponyms(synset):
    hyponyms = set()
    for hyponym in synset.hyponyms():
        hyponyms.union(set(_get_hyponyms(hyponym)))
    return hyponyms.union(set(synset.hyponyms()))


def get_hyponyms(w):
    """ return the wordlist of w's hyponyms"""
    wordset = set()
    for synset in wn.synsets(w):
        #import pdb; pdb.set_trace()
        wordset.union(_get_hyponyms(synset))

    # import pdb; pdb.set_trace()
    wordlist = []
    for ws in wordset:
        for lemma in ws.lemmas():
             #print lemma.name()
             wordlist.append(lemma.name())

    return list(set(wordlist))


def get_lemma(word):
    return wnl.lemmatize(word.lower(), pos='v')

def check_word_(strs, words):
    """ check the word is words list, and return the string"""
    #output=[]
    #output= OrderedDict()
    print "strs: ", strs

    #import pdb; pdb.set_trace()
    #for w in str(strs).split():
    #tokens = StanfordTokenizer().tokenize(strs)
    tokens = wordpunct_tokenize(strs)
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

    #print "tokens:", tokens
    #import pdb; pdb.set_trace()
    #return ' '.join(str(w) for w in output)
    return tokens


def check_word(sent, words):
    """ check the word is words list, and return the string """
    #output=[]
    #output= OrderedDict()
    print "check the sentence: ", sent

    tokens = []
    #tags = []
    if len(sent) > 0:
        #tags = get_pos(sent)
        tokens = rank._interface(sent, words)
    #print "tokens:", tokens
    return tokens

def get_pos(sent):
    #words = StanfordTokenizer().tokenize(str(sent))
    #tokens = st.tag(words)
    tokens = {}

    for tag in st.tag(StanfordTokenizer().tokenize(str(sent))):
        tokens[tag[0].lower()] = tag[1]

    return tokens

def _check_word(sent, tags, words):
    """ get the candidates of the difficult words """
    print "check the sentence: ", sent

    tokens = []
    if len(sent) > 0:
        tokens = rank._interface(sent, tags, words)

    #import pdb; pdb.set_trace()
    return tokens


def lemma_words(words):
    output=[]
    for w in words:
        _w = wnl.lemmatize(w.lower(), pos='v')


def get_wordnet_list(w):
    """ replace the words, using the synonyms  """
    #TODO: should limit the lemma number
    wordnet = []
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
