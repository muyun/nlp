# -*- coding: utf-8 -*-
#  
# deal with the dataset
#
# coding by wenlong 
#

from collections import OrderedDict

import openpyxl

#import nltk
from nltk.corpus import wordnet as wn
# lemma
from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()

#read the dataset
#filename = '/Users/zhaowenlong/workspace/proj/dev.nlp/web/simptext/wordlist.xlsx'

"""
Wb = openpyxl.load_workbook(filename)
sheet = wb.get_sheet_by_name('level 1')

#store the simplied words in the simp_words list
simp_words=[]
for x in range(1, sheet.max_row+1):
    simp_words.append(str(sheet.cell(row=x,column=1).value))

# now removing it
#TODO- the replace function
"""

def read_file(filename):
    """read the xlsx file and stored 1st column into words list"""
    #using the openpyxl lib here
    wb = openpyxl.load_workbook(filename)
    sheet = wb.get_sheet_by_name('level 1')

    #store the simplied words in the words list
    words=[]
    for x in range(1, sheet.max_row+1):
       words.append(str(sheet.cell(row=x,column=1).value).lower())

    # now removing it
    #TODO- the replace function
    return words


def check_word(strs, words):
    """ check the word is words list, and return the string"""
    #output={}
    output=OrderedDict()
    print "strs: ", strs

    #import pdb; pdb.set_trace()
    for w in str(strs).split():
        #_w = w.lower()
        _w = wnl.lemmatize(w.lower(), pos='v')
        #print "_w: ", _w
        if _w in words:
            output[w] = w
        else:
            output[w] = replace_word(_w)

    #import pdb; pdb.set_trace()
    #return ' '.join(str(w) for w in output)

    return output

def replace_word(w):
    """ replace the words, using WordNet """  
    #TODO: should limit the lemma number
    #wordnet = ['aa', 'bb']
    wordnet=[]
    print "w: " ,w
    for synset in wn.synsets(w):
        for lemma in synset.lemmas():
            #print lemma.name()
            wordnet.append(lemma.name())

    return list(set(wordnet))


# main test
#def main():
    
