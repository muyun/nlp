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

from nltk.parse.stanford import StanfordDependencyParser
eng_parser = StanfordDependencyParser(model_path=u'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')

import base

PUNCTUATION = (';', ':', ',', '.', '!', '?')
COMMA = ','

def simp_adverb_sent(tokens, node_list):
    strs = ""

    if COMMA not in tokens:
        return strs

    root = ""
    root_ind = node_list[0][4]['root'][0]
    for nd in node_list:
        if root_ind == nd[0]:
            root=nd[1]

    #split_ind = 0
    for nd in node_list[1:]:
        #import pdb; pdb.set_trace()
        #print(nd)
        if (root in nd) and ('advcl' in nd[4].keys() or 'xcomp' in nd[4].keys()):
            pass

        if (root in nd) and ('advcl' in nd[4].keys() or 'xcomp' in nd[4].keys()):
            #print "conj: ", nd
            #print "conj node: ", nd[4]['conj']

            #import pdb; pdb.set_trace()
            nsubj = ""
            nsubj_ind = 0
            if ('nsubj' in nd[4].keys()):
                nsubj_ind = nd[4]['nsubj'][0]
                
            advcl_dict = {}
            advcl_tag = ""
            if ('advcl' in nd[4].keys()):
                advcl_ind = nd[4]['advcl'][0]

                #import pdb; pdb.set_trace()
                #advcl_dict = {}
                for _nd in node_list: #BUG
                    if advcl_ind == _nd[0]:
                         advcl_dict = _nd[4]
                         advcl_tag = _nd[2]
                         break
                     
                verb = 'be'
                # TODO
                if advcl_tag == 'VBN':
                    nsubj = base.upper_first_char(tokens[nsubj_ind]) + " " + verb + " "
                if advcl_tag == 'VBG':
                    nsubj = base.upper_first_char(tokens[nsubj_ind]) + " "

                #ASSUME ',' is the splitting tag    
                split_ind = tokens.index(COMMA)
                    #nsubj_ind = nd[4]['nsubj'][0]
                    #if (advcl_ind < split_ind):
                    #subj = tokens[nsubj_ind]
                   # tokens.insert(1, base.upper_first_char(subj))

                _str1 = tokens[:(split_ind)]
                if _str1[-1] in PUNCTUATION:
                    _str1[-1] = ''
                str1 = nsubj + ' '.join(_str1)
                        #print "1st sent: ", str1

                        # upper the 1st char in 2nd sent
                    #tokens[nsubj_ind] = base.upper_first_char(tokens[nsubj_ind])
                _str2 = tokens[root_ind:]
                        #w = _w + ' '
                str2 = base.upper_first_char(tokens[nsubj_ind]) + " " + ' '.join(_str2)
                        #print "2nd sent: ", str2

                strs = str1 + ' . ' + str2

                return strs    

            #import pdb; pdb.set_trace()
            xcomp_ind = 0 
            if ('xcomp' in nd[4].keys()):
                xcomp_ind = nd[4]['xcomp'][0]

                #import pdb; pdb.set_trace()
                #advcl_dict = {}
                for _nd in node_list: #BUG
                    if xcomp_ind == _nd[0]:
                         xcomp_dict = _nd[4]
                         xcomp_tag = _nd[2]
                         break
                     
                verb = 'be'
                # TODO
                if xcomp_tag == 'VBN':
                    nsubj = base.upper_first_char(tokens[nsubj_ind]) + " " + verb + " "
                if xcomp_tag == 'VBG':
                    nsubj = base.upper_first_char(tokens[nsubj_ind]) + " "

                split_ind = tokens.index(COMMA)
                    #nsubj_ind = nd[4]['nsubj'][0]
                    #if (advcl_ind < split_ind):
                    #subj = tokens[nsubj_ind]
                   # tokens.insert(1, base.upper_first_char(subj))

                _str1 = tokens[:(split_ind)]
                if _str1[-1] in PUNCTUATION:
                    _str1[-1] = ''
                str1 = nsubj + ' '.join(_str1)
                        #print "1st sent: ", str1

                        # upper the 1st char in 2nd sent
                    #tokens[nsubj_ind] = base.upper_first_char(tokens[nsubj_ind])
                #_str2 = tokens[root_ind:]
                _str2 = tokens[split_ind+1:]
                        #w = _w + ' '
                #str2 = base.upper_first_char(tokens[nsubj_ind]) + " " + ' '.join(_str2)
                str2 = "That" + " " + ' '.join(_str2)
                        #print "2nd sent: ", str2

                strs = str1 + ' . ' + str2 + ' .'

                return strs
 

    return strs


def simp_syn_sent_(sent):
    strs = ""
    # the original tokens in the sent


    #import pdb; pdb.set_trace()
    #print(sent)
    #import pdb; pdb.set_trace()
    tokens = StanfordTokenizer().tokenize(str(sent))
    #tokens = wordpunct_tokenize(str(sent))
    tokens.insert(0, '')

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
    #strs = simp_coordi_sent(tokens, node_list)
    #strs = simp_subordi_sent(tokens, node_list)
    strs = simp_adverb_sent(tokens, node_list)
    #strs = simp_parti_sent(tokens, node_list)
    #strs = simp_adjec_sent(tokens, node_list)
    #strs = simp_appos_sent(tokens, node_list)
    #strs = simp_passive_sent(tokens, node_list)

    return strs

def main():
    #  clauses
    sent = "Needing money, I begged my parents."
    sent = "Peter came suprising everyone"
    
    #sent = "Refreshed, Peter stood up."

    #print(simp_coordi_sent(sent))
    print(simp_syn_sent_(sent))    

        
if __name__ == '__main__':
    main()

        
