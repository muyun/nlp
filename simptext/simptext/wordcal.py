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
from nltk.tokenize import wordpunct_tokenize
from nltk.tokenize import StanfordTokenizer
from nltk.tag import StanfordPOSTagger
st = StanfordPOSTagger('english-bidirectional-distsim.tagger')

# lemma
from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()

import string
import re

# the Models about the training model about the word rank
from models import rank

# about the supersense tagger
from sst import sst


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

def _check_word_(sent):
    """ check the word is words list, and return the string """
    #output=[]
    #output= OrderedDict()
    print "check the sentence: ", sent

    tokens = []
    #tags = []
    if len(sent) > 0:
        tokens = wordpunct_tokenize(sent)
        for ind in range(len(tokens)):
            tokens_dict = {}
            _output = []
            _output.append(tokens[ind])

            tokens_dict[tokens[ind]] = _output
            tokens[ind] = tokens_dict
            
    #print "tokens:", tokens
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
    

def map_word_supersense(w):
    wdict={}
    for synset in wn.synsets(w):
        #print(synset)
        #print(synset.lexname())

        #import pdb; pdb.set_trace()
        match = re.search(r'(\w+.\w.\d+)', str(synset)) # like Synset('gift.n.01')
        if match:
            wdict[synset.lexname()] = match.group()

    return wdict

def _get_sst(sent):
    _sst = ""
    filename = '_example'

    #import pdb; pdb.set_trace()
    sst_start = time.time()
    #write_file(_path+filename, sent)
    _sst = sst.exec_ssh(filename, sent)
    #import pdb; pdb.set_trace()
    print(_sst)
    sst_end = time.time()
    print "The time of sst function: ", sst_end - sst_start

    return _sst

    """
    dict_sst = {}
    #items = re.findall(r'(\w+\|\w+)', _sst) #['eats|consumption', 'apple|FOOD']
    items = _sst.split()
    for item in items:
        match = re.search(r'(\w+\|\w+)', item)
        if match:
            elems = match.group().split('|')
            dict_sst[elems[0]] = elems[1]

    #import pdb; pdb.set_trace()
    return dict_sst
    """
    

"""
    
def get_word_candidates(sent, s_dict):
    #
    lst = []

    _lst = []str
    for x in s_dict:
        if type(x) is dict:
            _lst.extend(x.keys())
        else:
            _lst.append(x)
    
    for w in sent.split():
        #import pdb; pdb.set_trace()
        if w in _lst:
            ind = _lst.index(w)
            lst.append(s_dict[ind])
        else:
            lst.append(w)

    return lst
"""

def get_word_candidates(sent, s_dict, referenced,wordlist):
    #named_entities_person, named_entities_org = chunk_sent_ner(sent)
    #print ("named_entities_person, named_entities_org")
    #print (named_entities_person, named_entities_org, sent)

    lst = []

    _lst = []
    for x in s_dict:
        if type(x) is dict:
            _lst.extend(x.keys())
        else:
            _lst.append(x)
    #print "_lst"
    #print _lst, s_dict

    sentence = chunk_sent(sent, s_dict, _lst)
    #print("sentence")
    #print (sentence)
    #print(sent)
    for w in sentence.split():
    #for w in sent.split():
        #import pdb; pdb.set_trace()
        #print("w, _lst")
        #print (w, _lst)
        if '_' in w:
            w = w.replace("_", " ")
        if w in _lst:

            print(w)
            ind = _lst.index(w)
            #print (referenced, s_dict[ind], w, sent)
            if s_dict[ind] == {w: [w, 'He','She']} or s_dict[ind] == {w: [w, 'She']} or s_dict[ind] == {w: [w, 'He']} or s_dict[ind] == {w: [w, 'They']} or s_dict[ind] == {w: [w, 'It'] }:
                if w in referenced:
                    lst.append(s_dict[ind])
                else:
                    lst.append(w)
                    referenced.append(w)
            else:
                lst.append(s_dict[ind])
        else:
            lst.append(w)

    return lst, referenced
    
def chunk_sent(sent, s_dict, _lst):
    for c in _lst:
        #print ("c")

        #ind = _lst.index(c)
        #print (c)
        if ' ' in c:
            #print ("c joinned")
            c_joinned = c.replace(" ", "_")
            sent = sent.replace(c,  c_joinned)
            #sent = sent.replace("_", " " )
            #print sent

    sentence =[]
    for w in sent.split():
        sentence.append(w)
    return " ".join(sentence)
   

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

def get_words(fin):
    words = []
    flist = open(fin,'r')
    ltines = flist.readlines()
    for l in ltines:
        if l:
            words.append(l.strip())
        else:
            break
    return words

"""
def cal_stat_info(filename):
    #filename="/Users/zhaowenlong/workspace/proj/dev.nlp/web/simptext/dataset/coinco/coinco_172.xml"

    lemmas = {}
    #import pdb; pdb.set_trace()
    [num_sentences, num_words, num_words_syn, lemmas] = get_stat_info(filename)

    return
"""
