# -*- coding: utf-8 -*-
#  
# deal with the dataset
#
# coding by wenlong 
#

import openpyxl
"""
from collections import OrderedDict

import string
"""
# Read the dataset
# filename = '/Users/zhaowenlong/workspace/proj/dev.nlp/web/simptext/wordlist.xlsx'

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

from bs4 import BeautifulSoup

import json

def read_xlsx_file(filename):
    """read the xlsx file and stored 1st column into words list"""
    # using the openpyxl lib here
    wb = openpyxl.load_workbook(filename)
    sheet = wb.get_sheet_by_name('level 1')

    # store the simplied words in the words list
    words = []
    for x in range(1, sheet.max_row+1):
        words.append(str(sheet.cell(row=x, column=1).value).lower())

    # now removing it
    # TODO- the replace function
    return tuple(words)


def read_xml_file(filename, word):
    """return the lemmas for the word in filename"""
    lemmas = []
    soup = BeautifulSoup(open(filename))

    # import pdb; pdb.set_trace()
    tokens = soup.find_all("token")
    for tk in tokens:
        # print tk
        if tk['lemma'] == word:
            lemmas.append(tk['lemma'])
            for st in tk.find_all("subst"):
                # print st['lemma']
                lemmas.append(st['lemma'])
    return tuple(lemmas)


def get_stat_info(filename, store_filename):

    num_sentence = 0
    num_words = 0
    num_words_syns = 0

    lemmas = {}
    
    soup = BeautifulSoup(open(filename))

    sentence = soup.find_all("targetsentence")
    num_sentence = len(sentence)

    tokens = soup.find_all("token")
    num_words = len(tokens)
    for tk in tokens:
        if tk['id'].isdigit():
            num_words_syns += 1

            lemmas[tk['wordform']] = []
            lemmas[tk['wordform']].append(tk['lemma'])
            for st in tk.find_all("subst"):
                #
                lemmas[tk['wordform']].append(st['lemma'])

    print "#sentence: ", num_sentence
    print "#words: ", num_words
    print "#words_syns: ", num_words_syns

    # write the file

    import pdb; pdb.set_trace()
    data = json.dump(lemmas, open(store_filename, 'wb'))
    
    return num_sentence, num_words, num_words_syns            


def get_simp_wordlist():
    return
# Main test
def main():
    filename = "/Users/zhaowenlong/workspace/proj/dev.nlp/web/simptext/dataset/coinco/coinco.xml"
    store_filename = "/Users/zhaowenlong/workspace/proj/dev.nlp/web/simptext/dataset/coinco/lemmas_.txt"
    info = get_stat_info(filename, store_filename)

if __name__ == '__main__':
    main()
