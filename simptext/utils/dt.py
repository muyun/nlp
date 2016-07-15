# -*- coding: utf-8 -*-
#  
"""
   utils.dt
   ~~~~~~~~~~
   data processing

@author wenlong
"""

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

import cal
#from . import cal

from collections import OrderedDict

#TODO: update the software construction
# for Roget's Thesaurus (1911)
import roget
#from data.roget import roget

def read_xlsx_file(filename, sheetnums):
    """read the xlsx file and stored first sheetnums into words list"""
    # using the openpyxl lib here
    wb = openpyxl.load_workbook(filename)

    #import pdb; pdb.set_trace()
    sheet_names = wb.get_sheet_names()[0:sheetnums]
    #sheet1 = wb.get_sheet_by_name('level 1')
    # sheet2 = wb.get_sheet_by_name('level 2')
    #sheet = wb.get_sheet_by_name(sheets_names)

    # store the simplied words in the words list
    words = []
    for sheet_name in sheet_names:
        worksheet=wb.get_sheet_by_name(sheet_name)
        for x in range(1, worksheet.max_row+1):
            words.append(str(worksheet.cell(row=x, column=1).value).lower())

    # now removing it
    # TODO- the replace function

    #import pdb; pdb.set_trace()
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
    """ read the filename and store the words with lemmas in store_filename"""

    num_words_syns = 0

    docs = OrderedDict() # store the info - docs[sentence] = [id,...]
    
    lemmas = {}  # store the word info - lemmas[id] = {word: synsets, ...}
    
    soup = BeautifulSoup(open(filename), "lxml")

    # number of sentences, based on the 'sent' tag
    sentences = soup.find_all("sent")
    num_sentences = len(sentences)

    # number of tokens, based on the 'token' tag
    num_tokens = len(soup.find_all("token"))

    #import pdb; pdb.set_trace()
    for sentence in sentences:
        # the key in docs is the target sentence
        target = str(sentence.targetsentence)
        docs[target] = []
        for tk in sentence.tokens.find_all("token"):
            #print(tk)
            if tk['id'].isdigit():
                num_words_syns += 1

                docs[target].append(tk['id'])

                #test_token[tk['id']]=tk['wordform']
                #_test_token.append(tk['wordform'])
                # the same word are stored in the same slot in the lemmas dict; A better data structure should be used
                
                lemmas[tk['id']] = []
                lemmas[tk['id']].append(tk['wordform'])
                lemmas[tk['id']].append(tk['lemma'])
                for st in tk.find_all("subst"):
                    lemmas[tk['id']].append(st['lemma'])

    #print "#sentence: ", num_sentence
    #print "#words: ", num_words
    #print "#words_syns: ", num_words_syns
    #print "#_test_token: ", len(_test_token)
    #print "#lemmas: ", len(lemmas)

    """
    for lst in _test_token:
        if lst in lemmas:
            pass
        else:
            print "lst: ", lst
    """

    """
    import pdb; pdb.set_trace()
    k = lemmas.keys()      
    k_feas = list(set(k) - set(_test_token))
    print(k_feas)                   
    """
    # write the file

    #write the fiel
    json.dump(lemmas, open(store_filename, 'w'))
    
    return num_sentences, num_tokens, num_words_syns, docs          


def print_intermedia(datafile, docs, wordlist):
    """print the intermedia data for the check
     @datafile is the lemmas dict filename
     @docs is the targetsentence
     @wordlist is the edb wordlist

    """
    data = json.load(open(datafile))

    # import pdb; pdb.set_trace()
    for sentence in docs.keys():
        #print(sentence)
        #print(docs[sentence])
        
        output = OrderedDict()
        for id in docs[sentence]:
            w = data[id][1] # the lemma of the wordform
            # remove the original word
            coincolist = data[id][1:]
            if w in coincolist:
                coincolist.remove(w)
            
            wordlist = cal.get_wordnet_list(w)
            if w in wordlist:
                wordlist.remove(w)

            feas = set(coincolist).intersection(wordlist)
            if len(feas) >= 1:
                k = '*'+data[id][0]
                output[k] = [coincolist, wordlist]
            else:
                output[data[id][0]] = [coincolist, wordlist]

        # write the sentence

        #import pdb; pdb.set_trace()
        with open('coinco_l1.json', 'a') as outfile:
            outfile.write('\n'+sentence+'\n')
            json.dump(output, outfile, indent=2)

    #json.dump(output, open('intermedia.json', 'w'))

        

def get_coinco_wordlist(datafile, wordlist):
    #
    num_simp_words = 0  # number of words from datafile and can be found in wordlist
    num_not_simp_words = 0
    _num_not_simp_words = 0

    num_feasible_words = 0
    
    # the words with synonyms that are not in EDB list
    not_simp_wordlist = []
    
    # load the dict from coinco dataset
    data = json.load(open(datafile))

    #_num = 0
    #import pdb; pdb.set_trace()
    for id in data.keys():
        #print data[k] # the word
        #_num += 1
        # TOUPDATE
        w = data[id][1].lower()
        if w in wordlist: # the lemma
            num_simp_words += 1
        else:
            num_not_simp_words += 1

            not_simp_wordlist.append(data[id][0]) # the words with synonyms not in EDB list

            # check whether the synonyms is in the ones in WordNet
            # the synonyms data[k]
            # the synonyms in mWordNet

            #import pdb; pdb.set_trace()
            k_wordnet_list = cal.get_wordnet_list(w)

            # we should remove the words not in EDB list

            k_simp_wordnet=[]
            for wd in k_wordnet_list:
                if wd in wordlist:
                      k_simp_wordnet.append(wd)
                      
            if len(k_simp_wordnet) >= 1:
                _num_not_simp_words += 1          
            #
            coincolist = data[id][1:]
            if w in coincolist:
                coincolist.remove(w)
            
            if w in k_simp_wordnet:
                k_simp_wordnet.remove(w)

            feas = set(coincolist).intersection(k_simp_wordnet)
            if len(feas) >= 1: #
                num_feasible_words += 1

    #
    #print "#num: ", _num
    #print "#num_simp_words: ", num_simp_words
    #print "#num_not_simp_words: ", num_not_simp_words
    #print "#words with feasible: ", num_feasible_words
    #import pdb; pdb.set_trace()
    if num_feasible_words == 0:
        ceiling = 0
    else:
        ceiling = num_feasible_words/float(num_not_simp_words)

    return num_simp_words, _num_not_simp_words, ceiling

def get_roget_info(datafile, wordlist):
    num_simp_words = 0  # number of words from roget and can be found in wordlist
    num_not_simp_words = 0
    _num_not_simp_words = 0

    num_feasible_words = 0
    
    # the words with synonyms that are not in EDB list
    not_simp_wordlist = []

    # load the dict from coinco dataset
    data = json.load(open(datafile))

    #_num = 0
    #import pdb; pdb.set_trace()
    for id in data.keys():
     #print data[k] # the word
        #_num += 1
        # TOUPDATE
        w = data[id][1].lower()
        if w in wordlist: # the lemma
            num_simp_words += 1
        else:
            num_not_simp_words += 1

            not_simp_wordlist.append(data[id][0]) # the words with synonyms not in EDB list

            # check whether the synonyms is in the ones in WordNet
            # the synonyms data[k]
            # the synonyms in mWordNet

            #import pdb; pdb.set_trace()
            #k_wordnet_list = cal.get_wordnet_list(w)
            k_wordnet_list = []
            for pos in roget.parts_of_speech:
                words = roget.all_entries(w, pos)

                for wd in words:
                    k_wordnet_list = k_wordnet_list + list(wd)


            k_simp_wordnet=[]
            for wd in k_wordnet_list:
                if wd in wordlist:
                      k_simp_wordnet.append(wd)
                      
            if len(k_simp_wordnet) >= 1:
                _num_not_simp_words += 1          
            #
            coincolist = data[id][1:]
            if w in coincolist:
                coincolist.remove(w)
            
            if w in k_simp_wordnet:
                k_simp_wordnet.remove(w)

            feas = set(coincolist).intersection(k_simp_wordnet)
            if len(feas) >= 1: #
                num_feasible_words += 1
                
    #
    #print "#num: ", _num
    #print "#num_simp_words: ", num_simp_words
    #print "#num_not_simp_words: ", num_not_simp_words
    #print "#words with feasible: ", num_feasible_words
    #import pdb; pdb.set_trace()
    if num_feasible_words == 0:
        ceiling = 0
    else:
        ceiling = num_feasible_words/float(_num_not_simp_words)

    return num_simp_words, _num_not_simp_words, ceiling


def get_semeval_info(datafile, wordlist):
    num_sentences = 0
    num_tokens = 0
    num_words_syns = 0
    tokens = {}
    #
    num_simp_words = 0  # number of words from datafile and can be found in wordlist
    simp_words = []
    num_not_simp_words = 0
    _num_not_simp_words = 0
    #not_simp_words = []

    num_feasible_words = 0
    feasible_words = []
    
    # the words with synonyms that are not in EDB list
    not_simp_wordlist = []
    _not_simp_wordlist = []
    
    # load the dict from semeval dataset
    #data = json.load(open(datafile))
    data = [line.strip() for line in open(datafile, 'r')]

    #_num = 0
    #import pdb; pdb.set_trace()
    for id in data:
        #print data[k] # the word
        #_num += 1
        # TOUPDATE
        wd_pos = id.split()
        w = wd_pos[0].split('.')[0]

        num_sentences += 1
        if w in tokens:
            tokens[w] = tokens[w] + 1
        else:
            tokens[w] = 0
        
        _w = w.lower()
        if _w in wordlist: # the lemma
            #num_simp_words += 1
            simp_words.append(w)
        else:
            #num_not_simp_words += 1
            #not_simp_words.append(w)

            not_simp_wordlist.append(w) # the words with synonyms not in EDB list

            # check whether the synonyms is in the ones in WordNet
            # the synonyms data[k]
            # the synonyms in mWordNet

            #import pdb; pdb.set_trace()
            #TODO: should check each word in k_wordnet_list is in EDB list
            k_wordnet_list = cal.get_wordnet_list(_w)
            k_simp_wordnet=[]
            for wd in k_wordnet_list:
                if wd in wordlist:
                      k_simp_wordnet.append(wd)

            #
            semevallist = id.split(':::')[1].strip().split(';')
            if w in semevallist:
                semevallist.remove(w)
            
            if w in k_simp_wordnet:
                k_simp_wordnet.remove(w)

            if len(k_simp_wordnet) >= 1:
                _not_simp_wordlist.append(w)

            feas = set(semevallist).intersection(k_simp_wordnet)
            if len(feas) >= 1: #
                feasible_words.append(w)
                #num_feasible_words += 1
                
    num_tokens = len(tokens)
    num_simp_words = len(set(simp_words))
    _num_not_simp_words = len(set(_not_simp_wordlist))
    num_feasible_words = len(set(feasible_words))
    #
    #print "#num: ", _num
    #print "#num_simp_words: ", num_simp_words
    #print "#num_not_simp_words: ", num_not_simp_words
    #print "#words with feasible: ", num_feasible_words
    #import pdb; pdb.set_trace()
    if num_feasible_words == 0:
        ceiling = 0
    else:
        ceiling = num_feasible_words/float(_num_not_simp_words)

    return num_sentences, num_tokens, num_simp_words, _num_not_simp_words, ceiling



def cal_ceiling(simp_wordlist):
    """calculate the ceiling"""
    #for word in simp_wordlist:
        # the synonyms in the coinco
        
    return

# Main test
def main():
    dir="/Users/zhaowenlong/workspace/proj/dev.nlp/simptext/dataset/"
    xlsx_filename = dir + "/wordlist.xlsx"
    
    filename = dir + "/coinco/coinco.xml"
    store_filename = dir + "/coinco/coinco_lemmas.txt"

    info = get_stat_info(filename, store_filename)
    print "#sentences: ", info[0]
    print "#words: ", info[1]
    print "#words marked with synonyms: ", info[2]
    #print "words with synonyms: ", info[3]

    # 
    wordlist = read_xlsx_file(xlsx_filename, 1)
    
    info_ = get_coinco_wordlist(store_filename, wordlist)
    print "#words in the EDB list for level 1: ", info_[0]
    print "#words not in the EDB list for level 1:: ", info_[1]
    print "The ceiling for level 1: ", info_[2]

    """
    wordlist = read_xlsx_file(xlsx_filename, 2)
    info_ = get_coinco_wordlist(store_filename, wordlist)
    print "#words in the EDB list for level 1+2: ", info_[0]
    print "#words not in the EDB list for level 1+2:: ", info_[1]
    print "The ceiling for level 1+2:: ", info_[2]
    # the feasible words
    
    wordlist = read_xlsx_file(xlsx_filename, 3)
    info_3 = get_coinco_wordlist(store_filename, wordlist)
    print "#words in the EDB list for level 1+2+3: ", info_3[0]
    print "#words not in the EDB list for level 1+2+3: ", info_3[1]
    print "The ceiling for level 1+2+3:: ", info_3[2]

    wordlist = read_xlsx_file(xlsx_filename, 4)
    info_4 = get_coinco_wordlist(store_filename, wordlist)
    print "#words in the EDB list for level 1+2+3+4: ", info_4[0]
    print "#words not in the EDB list for level 1+2+3+4: ", info_4[1]
    print "The ceiling for level 1+2+3+4: ", info_4[2]
    """
    # print the intermeida data
    #inter = print_intermedia(store_filename, info[3], wordlist)
    

    """
    # SemEval 2007
    #filename = dirname + "/semeval/trial/lexsub_trial.xml"
    filename = dirname + "/semeval/trial/BLoutof10.out"
    store_filename = dirname + "/semeval/trial/semeval_lemmas_.txt"
    
    xlsx_filename = dirname + "/wordlist.xlsx"
    wordlist = read_xlsx_file(xlsx_filename, 1)
    info_ = get_semeval_info(filename, wordlist)
    print "#sentences: ", info_[0]
    print "#words: ", info_[1]
    print "#words marked with synonyms: ", info_[1]
    #print "words with synonyms: ", info[3]
    print "#words in the EDB list for level 1: ", info_[2]
    print "#words not in the EDB list for level 1:: ", info_[3]
    print "The ceiling for level 1: ", info_[4]

    wordlist = read_xlsx_file(xlsx_filename, 2)
    info_ = get_semeval_info(filename, wordlist)
    print "#sentences: ", info_[0]
    print "#words: ", info_[1]
    print "#words marked with synonyms: ", info_[1]
    #print "words with synonyms: ", info[3]
    print "#words in the EDB list for level 1+2: ", info_[2]
    print "#words not in the EDB list for level 1+2: ", info_[3]
    print "The ceiling for level 1+2: ", info_[4]


    wordlist = read_xlsx_file(xlsx_filename, 3)
    info_ = get_semeval_info(filename, wordlist)
    print "#sentences: ", info_[0]
    print "#words: ", info_[1]
    print "#words marked with synonyms: ", info_[1]
    #print "words with synonyms: ", info[3]
    print "#words in the EDB list for level 1+2+3: ", info_[2]
    print "#words not in the EDB list for level 1+2+3: ", info_[3]
    print "The ceiling for level 1+2+3: ", info_[4]

    wordlist = read_xlsx_file(xlsx_filename, 4)
    info_ = get_semeval_info(filename, wordlist)
    print "#sentences: ", info_[0]
    print "#words: ", info_[1]
    print "#words marked with synonyms: ", info_[1]
    #print "words with synonyms: ", info[3]
    print "#words in the EDB list for level 1+2+3+4: ", info_[2]
    print "#words not in the EDB list for level 1+2+3+4: ", info_[3]
    print "The ceiling for level 1+2+3+4: ", info_[4]
    
    """

    # Mechanical Turk

    # roget
    #filename = dirname + "/data/roget"
    
    #
    """
    xlsx_filename = dirname + "/wordlist.xlsx"
   
    wordlist = read_xlsx_file(xlsx_filename, 1)
    info_ = get_roget_info(store_filename, wordlist)
    print "#words in the EDB list for level 1: ", info_[0]
    print "#words not in the EDB list for level 1:: ", info_[1]
    print "The ceiling for level 1: ", info_[2]

    wordlist = read_xlsx_file(xlsx_filename, 2)
    info_ = get_roget_info(store_filename, wordlist)
    print "#words in the EDB list for level 1+2: ", info_[0]
    print "#words not in the EDB list for level 1+2: ", info_[1]
    print "The ceiling for level 1+2: ", info_[2]

    wordlist = read_xlsx_file(xlsx_filename, 3)
    info_ = get_roget_info(store_filename, wordlist)
    print "#words in the EDB list for level 1+2+3: ", info_[0]
    print "#words not in the EDB list for level 1+2+3: ", info_[1]
    print "The ceiling for level 1+2+3: ", info_[2]

    wordlist = read_xlsx_file(xlsx_filename, 4)
    info_ = get_roget_info(store_filename, wordlist)
    print "#words in the EDB list for level 1+2+3+4: ", info_[0]
    print "#words not in the EDB list for level 1+2+3+4: ", info_[1]
    print "The ceiling for level 1+2+3+4: ", info_[2]
    
    
    """
    """
    lemmas = []
    wd ='mission'
    for pos in roget.parts_of_speech:

        import pdb; pdb.set_trace()
        words = roget.all_entries(wd, pos)
        for w in words:
            lemmas = lemmas + list(w)

    print lemmas
    """

if __name__ == '__main__':
     main()
