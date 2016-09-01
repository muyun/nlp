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
#from nltk.tokenize import wordpunct_tokenize

# use the wrapper or use the standard lib?
from nltk.parse.stanford import StanfordDependencyParser
eng_parser = StanfordDependencyParser(model_path=u'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')

#from  nltk.parse.stanford import StanfordParser
#eng_parser = StanfordParser(model_path=u'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')

#from alg import base
import base

PUNCTUATION = (';', ':', ',', '.', '!', '?')

def simp_adjec_sent(tokens, node_list):
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
    cop_ind = 0
    for nd in node_list:
        if root_ind == nd[0]:
            root=nd[1]
            if ('cop' in nd[4].keys()):
                cop_ind = nd[4]['cop'][0]

    # cop


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

            subj = tokens[nsubj_ind]
            nsubj_dict = {}
            for _nd in node_list[1:]: #BUG
                if nsubj_ind == _nd[0]:
                     nsubj_dict = _nd[4]
                     break

            # are
            cop_ind = 0
            if ('cop' in nd[4].keys()):
                cop_ind = nd[4]['cop'][0]

            #import pdb; pdb.set_trace()
            if ('acl:relcl' in nsubj_dict.keys()):
                #[NOTICE]: connect the nsubj + acl as 1st
                #import pdb; pdb.set_trace()
                relcl_ind = nsubj_dict['acl:relcl'][0]

                # is there the 'dobj'
                dobj_ind = 0
                rel_nsubj_ind = 0
                nmod_ind = 0
                for _nd in node_list[1:]:
                    if relcl_ind == _nd[0]:
                        if ('dobj' in _nd[4].keys()):
                            dobj_ind = _nd[4]['dobj'][0]
                        if ('nsubj' in _nd[4].keys()):
                            rel_nsubj_ind = _nd[4]['nsubj'][0]
                        if ('nmod' in _nd[4].keys()):
                            nmod_ind = _nd[4]['nmod'][0]
                        #break


                """
                TODO: The code cannot recognize the 'dobj' and 'nsubj'
                import pdb; pdb.set_trace()
                if dobj_ind != 0: # the verb is modified by "dobj"

                    #import pdb; pdb.set_trace()
                    rel_nsubj = base.upper_first_char(tokens[rel_nsubj_ind])
                    _str1 =  tokens[relcl_ind:(root_ind-1)]

                    if _str1[-1] in PUNCTUATION:
                       _str1[-1] = ''
                    str1 = rel_nsubj + " " + ' '.join(_str1) + " " + tokens[nsubj_ind]

                   # upper the 1st char in 2nd sent
                    _str2 = tokens[root_ind:]
                   #w = _w + ' '
                    if cop_ind > 0:
                        str2 = base.upper_first_char(subj) + " " + tokens[cop_ind] + " " + ' '.join(_str2)
                    else:
                        str2 = base.upper_first_char(subj) + " " + ' '.join(_str2)
                   #print "2nd sent: ", str2

                    strs = str1 + ' . ' + str2

                    return strs
                """

                #import pdb; pdb.set_trace()
                if nmod_ind != 0: # nmod
                    #import pdb; pdb.set_trace()
                    rel_nsubj = base.upper_first_char(tokens[rel_nsubj_ind])
                    _str1 =  tokens[relcl_ind:(root_ind-1)]

                    if len(_str1) > 0 and _str1[-1] in PUNCTUATION:
                       _str1[-1] = ''
                    str1 = rel_nsubj + " " + ' '.join(_str1) + " " + tokens[nsubj_ind]

                   # upper the 1st char in 2nd sent
                    _str2 = tokens[root_ind:]
                   #w = _w + ' '
                    if cop_ind > 0:
                        str2 = base.upper_first_char(subj) + " " + tokens[cop_ind] + " " + ' '.join(_str2)
                    else:
                        str2 = base.upper_first_char(subj) + " " + ' '.join(_str2)
                   #print "2nd sent: ", str2

                    strs = str1 + ' . ' + str2

                    return strs

                else: # nsubj
                #subj = tokens[nsubj_ind]
                #tokens.insert(1, upper_first_char(subj))

                    #TODO- cannot recognize the nsubj and dobj
                    #import pdb; pdb.set_trace()
                    root_ind = tokens.index(root)

                    if cop_ind:
                        _str1 = tokens[relcl_ind:cop_ind]
                    else:
                        _str1 = tokens[relcl_ind:root_ind]
                    if len(_str1) > 0 and _str1[-1] in PUNCTUATION:
                        _str1[-1] = ''
                    str1 = base.upper_first_char(subj) + " " + ' '.join(_str1)
                #print "1st sent: ", str1

                # upper the 1st char in 2nd sent
                    if cop_ind:
                        _str2 = tokens[cop_ind:]
                    else:
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
    strs = simp_adjec_sent(tokens, node_list)
    #strs = simp_appos_sent(tokens, node_list)
    #strs = simp_passive_sent(tokens, node_list)

    return strs

def main():
    # adjectival Clauses
    #sent = "Peter, who liked fruits, ate an apple."
    #sent = "I ate fish and he drank wine."
    sent = "The apple, which Peter ate, was red."
    sent = "Peter, whom I know, came."

    #sent = "Peter, to whom I talked, came."
    sent = "The books, most of which I read, are interesting."

    #print(simp_coordi_sent(sent))
    print(simp_syn_sent_(sent))


if __name__ == '__main__':
    main()
