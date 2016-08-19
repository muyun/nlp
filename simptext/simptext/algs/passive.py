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


def simp_passive_sent(tokens, node_list):
    """
    strs = ""
    # the original tokens in the sent


    #import pdb; pdb.set_trace()
    print(sent)
    #import pdb; pdb.set_trace()
    tokens = StanfordTokenizer().tokenize(str(sent))
    tokens.insert(0, '')

    result = list(eng_parser.raw_parse(sent))[0]
    root = result.root['word']

    #w = result.tree()
    #print "parse_tree:", w

    #TODO: use the tree structure, check again
    node_list = [] # dict (4 -> 4, u'said', u'VBD', u'root', [[18], [22], [16], [3]])
    for node in result.nodes.items():
        node_list.append(base.get_triples(node))
        #node_list[base.get_triples[0]] = base.get_triples(node)
    """
    root = ""
    root_ind = node_list[0][4]['root'][0]
    for nd in node_list:
        if root_ind == nd[0]:
            root=nd[1]

    strs = ""
    #split_ind = 0
    for nd in node_list[1:]:
        #import pdb; pdb.set_trace()
        #print(nd)
        # A passive nominal subjec
        if (root in nd) and ('nsubjpass' in nd[4].keys()):
            pass

        if (root in nd) and ('nsubjpass' in nd[4].keys()):
            #print "conj: ", nd
            #print "conj node: ", nd[4]['conj']

            #import pdb; pdb.set_trace()
            nsubjpass_ind = nd[4]['nsubjpass'][0]

            det_ind = 0
            subj = ""
            if ('nmod' in nd[4].keys()):
                nmod_ind = nd[4]['nmod'][0]

                nmod_dict = {}
                for _nd in node_list: #BUG
                    if nmod_ind == _nd[0]:
                         nmod_dict = _nd[4]
                         break


                #import pdb; pdb.set_trace()
            #if ('case' in nmod_dict.keys()): # 'by'
                #[NOTICE]: connect the nsubj + acl as 1st
                #import pdb; pdb.set_trace()
                if ('det' in nmod_dict):
                    det_ind = nmod_dict['det'][0]

                if det_ind:
                    subj = base.upper_first_char(tokens[det_ind]) + " " + tokens[nmod_ind]
                else:
                    subj = tokens[nmod_ind]

            strs = subj + " " + root + " " + tokens[nsubjpass_ind]
            """
                #[NOTICE]: remove the ',' after the nsubj
                if tokens[nsubj_ind + 1] in PUNCTUATION:
                    tokens[nsubj_ind + 1] = ''

                tokens.insert(nsubj_ind + 1, verb)

                #root_ind = tokens.index(root)
                #_str1 = tokens[nsubj_ind:root_ind]

                if _str1[-1] in PUNCTUATION:
                    _str1[-1] = ''
                str1 =  ' '.join(_str1)
                #print "1st sent: ", str1

                # upper the 1st char in 2nd sent
                _str2 = tokens[root_ind:]
                #w = _w + ' '
                str2 = upper_first_char(subj) + " " + ' '.join(_str2)
                #print "2nd sent: ", str2
            """
                #strs = str1 + ' . ' + str2
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
    #strs = simp_advcl_sent(tokens, node_list)
    #strs = simp_parti_sent(tokens, node_list)
    #strs = simp_adjec_sent(tokens, node_list)
    #strs = simp_appos_sent(tokens, node_list)
    strs = simp_passive_sent(tokens, node_list)

    return strs

def main():

    sent = "Peter was hit by a bus."
    #print(simp_coordi_sent(sent))
    print(simp_syn_sent_(sent))


if __name__ == '__main__':
    main()
