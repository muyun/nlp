# -*- coding: utf-8 -*-
import glob, lxml, re
from lxml import etree

import json

# clean the input
def clean(l):
    l = l.replace('<size=-1>','')
    l = l.replace('</size>','')
    l = l.replace('<br>','')
    l = l.replace('&','&amp;')
    l = l.replace('"<"','&lt;')
    l = l.replace('">"','&gt;')
    return l.rstrip(',;\n') + '\n'

# get information from the xml
def headword(class_element):
    return re.sub('[0-9#\[\] ]','',class_element.find("headword").find("b").text)

def pos(pos_element):
    return re.sub('[.#]','',pos_element.find("b").text)

def words(paragraph_element):
    return set([word.strip() for i in paragraph_element 
           if not i.text is None 
           for word in i.text.split(',') 
           if not word == ' '
           ])

def index(fn,root):
    return re.sub('[/Users/zhaowenlong/workspace/proj/dev.nlp/web/simptext/utils/data/roget/heads.txt]','',fn + ' ') + headword(root)

# helper generator:
def pospargen(c):
    for a,b in [c[x:x+2] for x in xrange(len(c)-1)]:
        if a.tag == 'pos' and b.tag == 'paragraph':
            yield [a,b]

# get list of [POS, [words,in,entry]]
def pos_words(c):
    return dict([[pos(a),words(b)] for a,b in pospargen(c)])

roget = {}

for fn in glob.glob("/Users/zhaowenlong/workspace/proj/dev.nlp/web/simptext/utils/data/roget/heads/head*.txt"):
    #import pdb; pdb.set_trace()
    with open(fn,'rb') as f:
        xml = ['<class>']+[clean(l) for l in f.readlines()]+['</class>']
        root = etree.fromstring(''.join(xml), parser=etree.XMLParser(encoding="windows-1252"))

        #import pdb; pdb.set_trace()
        roget[index(fn,root)] = pos_words(root.getchildren())

parts_of_speech = ['INT', 'VB', 'ADJ', 'N']


#import pdb; pdb.set_trace()
from collections import defaultdict

reverse_roget = defaultdict(set)

#lemmas = {} # for the file store

for category in roget: #head_file, like '_1 Existence'
    for pos in parts_of_speech:  #in prts_of_speech
        if pos in roget[category]:  # {'_1 Existence' : {'ADV' : set (['in point of fact', 'indeed'])}}
            for word in roget[category][pos]:
                reverse_roget[word + '_' + pos].add(category)

                
#import pdb; pdb.set_trace()
# INTERFACE COMMANDS
def categories(word,pos):  # entries means the filename
    "If you want to know which entries a word with a given part of speech occurs in"
    return reverse_roget[word + '_' + pos]

def common_categories(w1,w2,pos):
    "If you want to know which categories are shared by two words with a given part of speech"
    return reverse_roget[w1 + '_' + pos] & reverse_roget[w2 + '_' + pos]

def list_words(category,pos):
    "If you want to list the words with a given part of speech for an entry"
    return roget[category][pos]

def all_entries(word,pos):
    "If you want a list of lists, with each list containing the words for an entry"
    return [list_words(category,pos) for category in categories(word,pos)]

def shared_categories(l,pos):
    "If you want to know which categories are shared by a list of words with a given part of speech"
    return set.intersection(*[categories(w,pos) for w in l])


def store_file(filename):
    #
    #reverse_roget
    lemmas = {}
    #for the file store

    #import pdb; pdb.set_trace()
    for k in reverse_roget: #word_pos
        #print(k)
        word_pos = k.split("_")
        lemmas_lst = []
        for st in reverse_roget[k]: # set(['900 Courage', '744 Defiance'])
            #print(roget[st][word_pos[1]])
            wd_lst= list(roget[st][word_pos[-1]])
            lemmas_lst = lemmas_lst + wd_lst
    
        lemmas[word_pos[0]] = lemmas_lst

        #print(lemmas)

    json.dump(lemmas, open(filename, 'w'))

"""
def main():
    lemmas = []
    wd = 'end'
    for pos in parts_of_speech:
        import pdb; pdb.set_trace()
        words = all_entries(wd, pos)
        #print(all_entries('existing', pos))

        for w in words:
            lemmas = lemmas + list(w)

 
    print lemmas

    #filename="/Users/zhaowenlong/workspace/proj/dev.nlp/web/simptext/utils/data/roget/roget.json"
    #store_file(filename)        

    #TODO: store the wordlist -> word
    
if __name__ == '__main__':
    main()
"""
