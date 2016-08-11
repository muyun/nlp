# -*- coding: utf-8 -*-
"""
   utils.base
   ~~~~~~~~~~
   base common function
"""
#from itertools import chain
from collections import defaultdict

from nltk.tokenize import StanfordTokenizer

from nltk.parse.stanford import StanfordDependencyParser
eng_parser = StanfordDependencyParser(model_path=u'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')

import base

PUNCTUATION = (';', ':', ',', '.', '!', '?')

def simp_paratax_sent(tokens, node_list):

    root = ""
    root_ind = node_list[0][4]['root'][0]
    for nd in node_list:
        if root_ind == nd[0]:
            root=nd[1]

    #import pdb; pdb.set_trace()

    PUNCT = '-'

    strs = ""

    #punct_ind = 0
    if PUNCT in tokens:
        # the sentence contains the punctuation, split it
        inds = [ind for ind, token in enumerate(tokens) if token == PUNCT]

        #import pdb; pdb.set_trace()
        if (len(inds) >= 2):
            for ind in inds:
                tokens[ind] = ''

            _str1 = tokens[:inds[0]] + tokens[inds[1]:]
            str1 = " ".join(_str1)

            subj = base.upper_first_char(tokens[inds[0]+1])
            _str2 = tokens[inds[0]+2:inds[1]]
            str2 = subj + " " + " ".join(_str2)


            strs = str1  + " " + str2

    return strs

def simp_syn_sent_(sent):
    strs = ""
    # the original tokens in the sent


    #import pdb; pdb.set_trace()
    #print(sent)
    #import pdb; pdb.set_trace()
    tokens = StanfordTokenizer().tokenize(str(sent))
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
    #strs = simp_advcl_sent(tokens, node_list)
    #strs = simp_parti_sent(tokens, node_list)
    #strs = simp_adjec_sent(tokens, node_list)
    #strs = simp_appos_sent(tokens, node_list)
    #strs = simp_passive_sent(tokens, node_list)
    strs = simp_paratax_sent(tokens, node_list)

    return strs

def main():
    # coordinated clauses
    sent = "He held it out, and with a delighted \"Oh!\""
    #sent = "I ate fish and he drank wine."
    sent = "We haven't totally forgotten about it, but we're looking forward to this upcoming season."
    sent = "I ate fish or he drank wine."

    #sent = "I ate an apple and an orange."
    sent = "I ate an apple and an orange."
    sent = "Peter - nobody guessed it - showed up."
    #print(simp_coordi_sent(sent))
    print(simp_syn_sent_(sent))


if __name__ == '__main__':
    main()
