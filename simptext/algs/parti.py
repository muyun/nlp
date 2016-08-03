# -*- coding: utf-8 -*-
"""
  utils.alg
  ~~~~~~~~~~~
  syntacitc algs

@author wenlong
"""
import inspect

from nltk import Tree

from nltk.tokenize import StanfordTokenizer

# use the wrapper or use the standard lib?
from nltk.parse.stanford import StanfordDependencyParser
eng_parser = StanfordDependencyParser(model_path=u'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')

#from  nltk.parse.stanford import StanfordParser
#eng_parser = StanfordParser(model_path=u'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')

from alg import base

PUNCTUATION = (';', ':', ',', '.', '!', '?')


def simp_parti_sent(tokens, node_list):

    """
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
            if ('acl' in nsubj_dict.keys()):
                #[NOTICE]: connect the nsubj + acl as 1st
                # And the 1st end in the PUNC
                #import pdb; pdb.set_trace()
                acl_ind = nsubj_dict['acl'][0]

                #[NOTICE]: end the 1st sentence at the 'punc' place after acl_ind
                # this assumation is wrong
                """
                for punc in PUNCTUATION:
                    if punc in tokens[acl_ind:]:
                        split_ind = tokens[acl_ind:].index(punc)
                        break
                """

                subj = tokens[nsubj_ind]
                #tokens.insert(1, upper_first_char(subj))

                #import pdb; pdb.set_trace()
                verb = "be"
                root_ind = tokens.index(root)
                _str1 = tokens[acl_ind:root_ind]
                if _str1[-1] in PUNCTUATION:
                    _str1[-1] = ''
                str1 = base.upper_first_char(subj) + " " + verb + " "
                str1 =  str1 + ' '.join(_str1)
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
    strs = simp_parti_sent(tokens, node_list)
    #strs = simp_adjec_sent(tokens, node_list)
    #strs = simp_appos_sent(tokens, node_list)
    #strs = simp_passive_sent(tokens, node_list)

    return strs


def main():
    # participial clauses
    sent = "Alicia, running down the street, tripped."

    sent = "Peter, also called Pete, came."

    #print(simp_coordi_sent(sent))
    print(simp_syn_sent_(sent))


if __name__ == '__main__':
    main()
