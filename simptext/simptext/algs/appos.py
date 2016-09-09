# -*- coding: utf-8 -*-
"""
   algs.appos
   ~~~~~~~~~~
   appos function
"""
#from itertools import chain
from collections import defaultdict

from nltk.tokenize import StanfordTokenizer
#from nltk.tokenize import wordpunct_tokenize

from nltk.parse.stanford import StanfordDependencyParser
eng_parser = StanfordDependencyParser(model_path=u'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')

#The girls, on the city, like it .import base
#from algs import base
import base

PUNCTUATION = (';', ':', ',', '.', '!', '?')

def simp_appos_sent(tokens, node_list):
    """
    strs = ""
    # the original tokens in the sent
    tokens = StanfordTokenizer().tokenize(sent)
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
        if (root in nd) and ('nsubj' in nd[4].keys()):
            pass

        if (root in nd) and ('nsubj' in nd[4].keys()):
            #print "conj: ", nd
            #print "conj node: ", nd[4]['conj']

            #import pdb; pdb.set_trace()
            nsubj_ind = nd[4]['nsubj'][0]
            nsubj_dict = {}
            for _nd in node_list: #BUG
                if nsubj_ind == _nd[0]:
                     nsubj_dict = _nd[4]
                     break


            #import pdb; pdb.set_trace()
            if ('appos' in nsubj_dict.keys()):
                #[NOTICE]: connect the nsubj + acl as 1st
                #import pdb; pdb.set_trace()
                appos_ind = nsubj_dict['appos'][0]

                verb = "is"
                #verb = base.update_vb_conjugation(verb, root)

                subj = base.upper_first_char(tokens[nsubj_ind])

                #[NOTICE]: remove the ',' after the nsubj
                if tokens[nsubj_ind + 1] in PUNCTUATION:
                    tokens[nsubj_ind + 1] = ''

                tokens.insert(nsubj_ind + 1, verb)

                root_ind = tokens.index(root)
                # SO bad solution, if the root isnot a 'verb'
                split_ind = 0
                if ',' in tokens:
                    split_ind = tokens.index(',')

                if tokens[root_ind] > split_ind:
                    _str1 = tokens[nsubj_ind:split_ind]
                    tokens[split_ind] = ''

                    if len(_str1) > 0 and _str1[-1] in PUNCTUATION:
                        _str1[-1] = ''
                    str1 =  ' '.join(_str1)

                    _str2 = tokens[split_ind:]
                    str2 = base.upper_first_char(subj) + " " + ' '.join(_str2)
                else:
                    _str1 = tokens[nsubj_ind:root_ind]

                    if len(_str1) > 0 and _str1[-1] in PUNCTUATION:
                        _str1[-1] = ''
                    str1 =  ' '.join(_str1)
                    #print "1st sent: ", str1

                    # upper the 1st char in 2nd sent
                    _str2 = tokens[root_ind:]
                    #w = _w + ' '
                    str2 = base.upper_first_char(subj) + " " + ' '.join(_str2)
                    #print "2nd sent: ", str2

                strs = str1 + ' . ' + str2
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
    strs = simp_appos_sent(tokens, node_list)
    #strs = simp_passive_sent(tokens, node_list)

    return strs

def main():
    # Appositive clauses

    #sent = "I ate an apple and an orange."
    sent = "I ate an apple and an orange."
    sent = "Peter, my son, ate an apple."
    sent = "Peter, my friend, likes it."
    sent = "Boys, my friends, like it."
    #sent = "Faizabad, the headquarters of Faizabad District, is a municipal board in the state of Uttar Pradesh , India ."
    #TODO: the tense of the output
    print(simp_syn_sent_(sent))


if __name__ == '__main__':
    main()
