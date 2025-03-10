# -*- coding: utf-8 -*-
"""
   utils.base
   ~~~~~~~~~~
   base common function
"""
#from itertools import chain
from collections import defaultdict

from nltk.tokenize import StanfordTokenizer
#from nltk.tokenize import wordpunct_tokenize

#from nltk.tag import StanfordPOSTagger
#eng_tagger = StanfordPOSTagger('english-bidirectional-distsim.tagger')

from nltk.parse.stanford import StanfordDependencyParser
eng_parser = StanfordDependencyParser(model_path=u'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')

from pattern.en import tenses, conjugate

#from algs import base
import base
#PUNCTUATION = (';', ':', ',', '.', '!', '?')
import time

def check_tag(word, node_list):
    """ get the tagger of the word in taggers, or return "" """
    taggers = []
    for nd in node_list[1:]:
        taggers.append((nd[1], nd[2]))
        
    for w, tagger in taggers:
        if w == word:
            return tagger
    return ""    

def simp_punct_sent(tokens, node_list):
    start_time = time.time()
    """
    tokens = StanfordTokenizer().tokenize(sent)
    tokens.insert(0, '')

    result = list(eng_parser.raw_parse(sent))[0]
    root = result.root['word']


    node_list = [] #(4, u'said', u'VBD', u'root', [[18], [22], [16], [3]])
    for node in result.nodes.items():
        #print(node)
        node_list.append(base.get_triples(node))

    # construct the tree
    #w = result.tree()
    #partial = Tree(w[parent].label(), )
    _subtree = {}
    for subtree in w.subtrees():
        #import pdb; pdb.set_trace()
        #traverse(subtree)
        _subtree[subtree.label()] = subtree

    """
    
    #PUNCTUATION = [';', ':', '-']
    PUNCTUATION = [';', ':']

    root = ""
    root_ind = node_list[0][4]['root'][0]
    for nd in node_list:
        if root_ind == nd[0]:
            root=nd[1]

    #import pdb; pdb.set_trace()

    strs = ""
    # "bugs" here
    pron = "They"
    verb = "are"
    #verb = conjugate(verb, tenses(root)[0][0], 3)
    #taggers_start = time.time()
    #taggers = eng_tagger.tag(tokens)
    
    #taggers_end = time.time()
    #taggers_during = taggers_end - taggers_start
    #print "The time of taggers_during: ", taggers_during
    
    punct_ind = 0
    punct_set = set(PUNCTUATION).intersection(set(tokens))

    #import pdb; pdb.set_trace()
    if len(punct_set) > 0:
        # the sentence contains the punctuation, split it
        for ind, token in enumerate(tokens):
            if token in PUNCTUATION:
                tokens[ind] = ' .' # remove the punctuation
                # if the 2nd sentence is a noun
                word = tokens[ind+1]

                """
                import pdb; pdb.set_trace()
                if 'NN' in check_tag(word, node_list):
                    # a pronoun and verb be added
                    tokens.insert(ind+1, verb)
                    tokens.insert(ind+1, pron)
                """
                
                tokens[ind+1] = base.upper_first_char(tokens[ind+1]) # upper the next word
                punct_ind = ind 
                
                #break

        #import pdb; pdb.set_trace()
        str1 = " ".join(tokens[:punct_ind])
        str2 = " ".join(tokens[punct_ind:])
        
        strs = str1  + str2

    end_time = time.time()
    during_time = end_time - start_time
    print "The time of punct function: ", during_time
    return strs

def simp_syn_sent_(sent):
    strs = ""
    # the original tokens in the sent


    #import pdb; pdb.set_trace()
    #print(sent)
    #import pdb; pdb.set_trace()
    tokens = StanfordTokenizer().tokenize(str(sent))
    #tokens = wordpunct_tokenize(str(sent))


    #import pdb; pdb.set_trace()
    tokens.insert(0, '')

    #taggers = eng_tagger.tag(sent.split())
    
    result = list(eng_parser.raw_parse(sent))[0]
    root = result.root['word']

    #w = result.tree()
    #print "parse_tree:", w
    #for row in result.triples():
    #    print(row)


    #import pdb; pdb.set_trace()
    #TODO: use the tree structure, check again
    node_list = [] # dict (4 -> 4, u'said', u'VBD', u'root', [[18], [22], [16], [3]])
    for node in result.nodes.items():
        node_list.append(base.get_triples(node))
        #node_list[base.get_triples[0]] = base.get_triples(node)


    #import pdb; pdb.set_trace()
    strs = simp_punct_sent(tokens, node_list)
    #strs = simp_subordi_sent(tokens, node_list)
    #strs = simp_advcl_sent(tokens, node_list)
    #strs = simp_parti_sent(tokens, node_list)
    #strs = simp_adjec_sent(tokens, node_list)
    #strs = simp_appos_sent(tokens, node_list)
    #strs = simp_passive_sent(tokens, node_list)

    return strs

def main():
    # punctuation clauses

    sent = "I ate fish; he drank wine. "
    #sent = "I have two brothers: they both live in China."
    #sent = "I have two brothers: Peter and Sam."
    #sent = "In March 1992 , Linux version 0.95 was the first to be capable of running X : This large version number jump was due to a feeling that a version 1.0 with no major missing pieces was imminent ."
    #sent = "This is a test ."
    sent = "I ate fish; raymond drank wine. "
    sent = "I have two brothers: they both live in China."
    sent = "I ate fish and Peter drank wine."
    sent = "Since he was hungry, he ate a banana."
    print(simp_syn_sent_(sent))    

        
if __name__ == '__main__':
    main()

        
