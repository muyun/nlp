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


# Main test
#def main():
    
