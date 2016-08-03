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

from alg import base

PUNCTUATION = (';', ':', ',', '.', '!', '?')

def simp_subordi_sent(tokens, node_list):
    # C1 and C2  must have the own subject
    #PUNCT = ','
    # the subordinating conjunction
    dict1 = {   'after': 'Then',
                'although': 'But',
                'though': 'But',
                'since': 'Therefore',
                'because': 'Therefore',
                'as': 'Therefore'
            }

    dict2 = {'so': 'So',
             'before': 'Then'
            }

    root = ""
    root_ind = node_list[0][4]['root'][0]
    for nd in node_list:
        if root_ind == nd[0]:
            root=nd[1]

    strs = ""
    #split_ind = 0
    mark_ind = 0
    for nd in node_list[1:]:
        #import pdb; pdb.set_trace()
        #print(nd)
        if (root in nd) and ('advcl' in nd[4].keys()):
            # C1 and C2 have its own subject
            
            #print "conj: ", nd
            #print "conj node: ", nd[4]['conj']
            pass

        if (root in nd) and ('advcl' in nd[4].keys()):
            advcl_ind = nd[4]['advcl'][0]

            #import pdb; pdb.set_trace()
            mark_list = []
            
            nsubj_ind = 0
            nsubj_word = ""
            if ('nsubj' in nd[4].keys()):
                nsubj_ind = nd[4]['nsubj'][0]
                for _nd in node_list[1:]:
                    if nsubj_ind == _nd[0]:
                        nsubj_word = _nd[1]
                        break

            advcl_dict = {}
            for _nd in node_list[1:]: #BUG
                if advcl_ind == _nd[0]:
                     advcl_dict = _nd[4]
                     mark_list = _nd
                     break
                 
            # the nsubj of the advcl
            nsubj_advcl_word = ""
            if ('nsubj' in advcl_dict.keys()):
                nsubj_advcl_ind = advcl_dict['nsubj'][0]
                for __nd in node_list[1:]:
                    if nsubj_advcl_ind == __nd[0]:
                        nsubj_advcl_word = __nd[1] # get the subj of the advcl
                        break

            if nsubj_word == nsubj_advcl_word:
                return strs
           

            #import pdb; pdb.set_trace()
            if ('mark' in advcl_dict.keys()):
                #import pdb; pdb.set_trace()
                mark_ind = mark_list[4]['mark'][0]
                marker = tokens[mark_ind].lower()

                # get the marker,  delete the conjunction
                #tokens[mark_ind] = ''
                #tokens[mark_ind+1] = upper_first_char(tokens[mark_ind+1])
                # if the marker is in the dict1
                # [NOTICE]: we use the punctuation to check the sentence
                if (marker in dict1.keys()): # if dict1, subordinated clause goes first
                    # delete the conjunction,
                    _w = dict1[marker]
                    tokens[mark_ind] = ''
                    tokens[mark_ind+1] = base.upper_first_char(tokens[mark_ind+1])

                    #[NOTICE]: we consider 1st ',' to split the sentence, and get the 2nd sentence

                    #import pdb; pdb.set_trace()
 

                    if nsubj_ind != 0:
                        _str1 = tokens[:(nsubj_ind)]
                        if _str1[-1] in PUNCTUATION:
                            _str1[-1] = ''
                        str1 = ' '.join(_str1)
                    #print "1st sent: ", str1

                        _str2 = tokens[nsubj_ind:]
                    #w = _w + ' '
                        str2 = _w + ' ' + ' '.join(_str2)
                    #print "2nd sent: ", str2

                        strs = str1 + ' . ' + str2

                    else:
                        pass

                    return strs


                # if dict2, the subordinated clause goes second
                if (marker in dict2.keys()):
                    _w = dict2[marker]
                    tokens[mark_ind] = ''
                    tokens[mark_ind+1] = base.upper_first_char(tokens[mark_ind+1])

                    #TODO add it before the nsubj
                    if nsubj_ind != 0:
                        _str1 = tokens[:(nsubj_ind)]
                        if _str1[-1] in PUNCTUATION:
                            _str1[-1] = ''

                        str1 = ' '.join(_str1)
                    #print "1st sent: ", str1

                        _str2 = tokens[nsubj_ind:]
                    #w = _w + ' '
                        str2 = _w + ' ' + ' '.join(_str2)
                    #print "2nd sent: ", str2

                        strs = str1 + ' . ' + str2
                    else:
                        pass

                    return strs


        #if mark_ind == 0:  # if no mark word
        # adverbial clauses [NOTICE]: consider ',' to split the sentence

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
    strs = simp_subordi_sent(tokens, node_list)
    #strs = simp_advcl_sent(tokens, node_list)
    #strs = simp_parti_sent(tokens, node_list)
    #strs = simp_adjec_sent(tokens, node_list)
    #strs = simp_appos_sent(tokens, node_list)
    #strs = simp_passive_sent(tokens, node_list)

    return strs

def main():
    #  clauses
    sent = "Since he came, I left"
    sent = "Before he came, I left"
    sent = "I feel angry when provoked"

    #print(simp_coordi_sent(sent))
    print(simp_syn_sent_(sent))    

        
if __name__ == '__main__':
    main()

        
