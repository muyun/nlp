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
from nltk.tag import StanfordNERTagger
eng_tagger = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')

#from algs import base
import base
import time

PUNCTUATION = (';', ':', ',', '.', '!', '?')

def simp_adjec_sent(tokens, node_list):
    start_time = time.time()
    """
    strs = ""
    # the original tokens in the sent
    tokens = StanfordTokenizer().tokenize(sent)
    tokens.insert(0, '')

    result = list(eng_parser.raw_parse(sent))[0]
    root = result.root['word']

    #w = result.tree()
    #print "parse_tree:",

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
    taggers = []
    for nd in node_list[1:]:
        taggers.append((nd[1], nd[2]))

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
            nsubj_compound_list = []
            amod_list = []
            nsubj_dict = {}
            det_ind = 0
            for _nd in node_list: #BUG
                if nsubj_ind == _nd[0]:
                     nsubj_dict = _nd[4]
                     if ('amod' in nsubj_dict.keys()):
                         amod_list = nsubj_dict['amod']
                     if ('compound' in nsubj_dict.keys()):
                         nsubj_compound_list = nsubj_dict['compound']
                     if ('det' in nsubj_dict.keys()):
                         det_ind = nsubj_dict['det'][0]
                     #break

            #nsubj = tokens[nsubj_ind]
            # get the nsubj
            nsubj = ""
            #import pdb; pdb.set_trace()
            for j in amod_list:
                nsubj = nsubj + " " + tokens[j]
            for i in nsubj_compound_list:
                nsubj = nsubj + " " + tokens[i]
            if det_ind > 0:
                nsubj = tokens[det_ind] + " " + nsubj + " " + tokens[nsubj_ind]
            else:
                nsubj = nsubj + " " + tokens[nsubj_ind]
            #nsubj = nsubj + " " + tokens[nsubj_ind]
            nsubj = nsubj[0].upper() + nsubj[1:]

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
                det_ind = 0
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
                #import pdb; pdb.set_trace()
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
                    case_ind = 0
                    for _nd in node_list[1:]:
                        if nmod_ind == _nd[0]:
                            if ('case' in _nd[4].keys()):
                                case_ind = _nd[4]['case'][0]

                    #import pdb; pdb.set_trace()
                    rel_nsubj = base.upper_first_char(tokens[rel_nsubj_ind])
                    _str1 =  tokens[relcl_ind:(root_ind-1)]

                    if len(_str1) > 0 and _str1[-1] in PUNCTUATION:
                       _str1[-1] = ''
                    str1 = rel_nsubj + " " + ' '.join(_str1) + " " + tokens[case_ind] + " " + nsubj.lower()

                   # upper the 1st char in 2nd sent
                    _str2 = tokens[root_ind:]
                   #w = _w + ' '
                    nsubj = nsubj.strip()
                    if cop_ind > 0:
                        #str2 = base.upper_first_char(nsubj) + " " + tokens[cop_ind] + " " + ' '.join(_str2)
                        str2 = nsubj + " " + tokens[cop_ind] + " " + ' '.join(_str2)
                    else:
                        #str2 = base.upper_first_char(nsubj) + " " + ' '.join(_str2)

                        str2 = nsubj + " " + ' '.join(_str2)
                   #print "2nd sent: ", str2

                    str2 = base.upper_first_char(str2)
                    strs = str2 + ' ' + str1 + " ."

                    #return strs

                else: # nsubj
                #subj = tokens[nsubj_ind]
                #tokens.insert(1, upper_first_char(subj))

                    #TODO- cannot recognize the nsubj and dobj
                    #import pdb; pdb.set_trace()
                    root_ind = tokens.index(root)

                    rel_nsubj = base.upper_first_char(tokens[rel_nsubj_ind])

                    #relcl_ind = nsubj_dict['acl:relcl'][0]

                    # is there the 'dobj'
                    relcl_dobj_ind = 0
                    for _nd in node_list[1:]:
                        if relcl_ind == _nd[0]:
                            if ('dobj' in _nd[4].keys()):
                                relcl_dobj_ind = _nd[4]['dobj'][0]

                    relcl_nmod_ind = 0
                    if relcl_dobj_ind != 0:
                        for _nd in node_list[1:]:
                            if relcl_dobj_ind == _nd[0]:
                                if ('nmod' in _nd[4].keys()):
                                    relcl_nmod_ind = _nd[4]['nmod'][0]


                    #import pdb; pdb.set_trace()
                    dobj = ""
                    if relcl_dobj_ind != 0:
                        if relcl_nmod_ind != 0:
                            dobj = ' '.join(tokens[relcl_dobj_ind:relcl_nmod_ind])
                        #else:
                        #    dobj = tokens[relcl_dobj_ind]

                    #_str1 =  tokens[relcl_ind:(root_ind-1)]

                    if cop_ind:
                        _str1 = tokens[relcl_ind:cop_ind]
                    else:
                        _str1 = tokens[relcl_ind:root_ind]

                    if len(_str1) > 0 and _str1[-1] in PUNCTUATION:
                        _str1[-1] = ''

                    #str1 = base.upper_first_char(nsubj) + " " + ' '.join(_str1)
                    if dobj:
                        #str1 = rel_nsubj + " " + ' '.join(_str1) + " " + dobj.lower()
                        str1 = rel_nsubj + " " + ' '.join(_str1) + " " + dobj.lower() + " " + nsubj.lower() #Bugs
                    else:
                        if rel_nsubj.lower() == 'who':
                            str1 = nsubj + " " + ' '.join(_str1)
                        else:
                            str1 = rel_nsubj + " " + ' '.join(_str1) + " " + nsubj.lower()
                        #str1 = nsubj + " " + ' '.join(_str1)
                    #print "1st sent: ", str1

                # upper the 1st char in 2nd sent
                    if cop_ind:
                        _str2 = tokens[cop_ind:]
                    else:
                        _str2 = tokens[root_ind:]
                #w = _w + ' '

                    str2 = base.upper_first_char(nsubj) + " " + ' '.join(_str2)
                    #print "2nd sent: ", str2

                    strs = str2 + " " + str1 + " ."
                    #return strs

    end_time = time.time()
    during_time = end_time - start_time
    print "The time of adjec function: ", during_time
    return strs

def simp_syn_sent_(sent):
    strs = ""
    # the original tokens in the sent
    """
    lst1 = "Peter, who liked fruits, ate an apple.".split()
    _lst = sent.split()

    #import pdb; pdb.set_trace()
    if lst1 == _lst:
        return "Peter liked fruits. Peter ate an apple."
    """
    #import pdb; pdb.set_trace()
    #print(sent)
    #import pdb; pdb.set_trace()
    tokens = StanfordTokenizer().tokenize(str(sent))
    #tokens = wordpunct_tokenize(str(sent))
    tokens.insert(0, '')

    result = list(eng_parser.raw_parse(sent))[0]
    root = result.root['word']


    #import pdb; pdb.set_trace()
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
    sent = "Peter, who liked fruits, ate an apple."
    #sent = "I ate fish and he drank wine."
    #sent = "The apple, which Peter ate, was red."
    #sent = "Alice emith, whom I know, came."

    #sent = "alice emitch, to whom I talked, came."
    #sent = "The books, most of which I read, are interesting."
    #sent = "Dodd simply retained his athletic director position , which he had acquired in 1950 ."

    #sent = "At present it is formed by the Aa , which descends from the Rigi and enters the southern extremity of the lake ."
    #print(simp_coordi_sent(sent))
    print(simp_syn_sent_(sent))


if __name__ == '__main__':
    main()
