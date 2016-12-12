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

from nltk.tag import StanfordNERTagger
eng_tagger = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')

#The girls, on the city, like it .import base
#from algs import base
import base
import time

from pattern.en import tenses, conjugate

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
    start_time = time.time()

    root = ""
    root_ind = node_list[0][4]['root'][0]
    for nd in node_list:
        if root_ind == nd[0]:
            root=nd[1]

    """
    taggers = []
    for nd in node_list[1:]:
        taggers.append((nd[1], nd[2]))
    """
    strs = ""
    #split_ind = 0
    for nd in node_list[1:]:
        #import pdb; pdb.set_trace()
        #print(nd)
        if (root in nd) and ('nsubj' in nd[4].keys() or ('nsubjpass' in nd[4].keys())):
            pass

        if (root in nd) and ('nsubj' in nd[4].keys() or ('nsubjpass' in nd[4].keys())):
            #print "conj: ", nd
            #print "conj node: ", nd[4]['conj']
            nsubj = ""
            nsubj_ind = 0
            nsubj_nmod_ind = 0
            nsubj_dict = {}
            #import pdb; pdb.set_trace()
            if ('nsubj' in nd[4].keys()):
                nsubj_ind = nd[4]['nsubj'][0]
                nsubj_compound_list = []
                #nsubj_nmod_ind = 0
                for _nd in node_list[1:]: #BUG
                    if nsubj_ind == _nd[0]:
                        nsubj_dict = _nd[4]
                        if ('compound' in nsubj_dict.keys()):
                            nsubj_compound_list = nsubj_dict['compound']
                        #break
                        if ('nmod' in nsubj_dict.keys()):
                            nsubj_nmod_ind=nsubj_dict['nmod'][0]

                #import pdb; pdb.set_trace()
                for i in nsubj_compound_list:
                    nsubj = nsubj + " " + tokens[i]

                cop_ind = 0
                for _nd in node_list[1:]:
                    if (root in _nd) and ('cop' in _nd[4].keys()):
                        cop_ind = _nd[4]['cop'][0]

            # get the nsubj
            #import pdb; pdb.set_trace()

            auxpass_ind = 0
            if ('nsubjpass' in nd[4].keys()):
                nsubj_ind = nd[4]['nsubjpass'][0]
                for _nd in node_list:
                    if root_ind == _nd[0] and  ('auxpass' in _nd[4].keys()):
                        auxpass_ind = nd[4]['auxpass'][0]

            if nsubj_nmod_ind != 0: #BUG here
                nsubj = " ".join(tokens[nsubj_ind:nsubj_nmod_ind+1])
            else:
                nsubj = nsubj + " " + tokens[nsubj_ind]

            nsubj = nsubj.strip()
            nsubj = nsubj[0].upper() + nsubj[1:] + " "

            """
            person_taggers = []
            org_taggers = []
            # replace the nsubj with "he/she"
            for token, title in taggers:
                if token in nsubj:
                    if title == 'PERSON':
                        person_taggers.append(token)
                    elif title == 'ORGANIZATION':
                        org_taggers.append(token)
                    else:
                        org_taggers.append(token)
            """
            #import pdb; pdb.set_trace()
            if len(nsubj_dict)>0 and ('appos' in nsubj_dict.keys()):
                #[NOTICE]: connect the nsubj + acl as 1st
                #import pdb; pdb.set_trace()
                appos_ind = nsubj_dict['appos'][0]

                #verb = "is"
                verb = conjugate("was", tenses(root)[0][0], 3)
                #verb = base.update_vb_conjugation(verb, root)

                #nsubj = base.upper_first_char(tokens[nsubj_ind])

                #[NOTICE]: remove the ',' after the nsubj
                if tokens[nsubj_ind + 1] in PUNCTUATION:
                    tokens[nsubj_ind + 1] = ''

                #tokens.insert(nsubj_ind + 1, verb)

                root_ind = tokens.index(root)
                # SO bad solution, if the root isnot a 'verb'
                split_ind = 0
                if ',' in tokens:
                    split_ind = tokens.index(',')

                for nd in node_list[1:]: #BUG
                    if nsubj_ind == nd[0]:
                     nsubj_dict = _nd[4]
                     if ('compound' in nsubj_dict.keys()):
                         nsubj_compound_list = nsubj_dict['compound']
                     #break
                     if ('nmod' in nsubj_dict.keys()):
                         nsubj_nmod_ind=nsubj_dict['nmod'][0]

                #import pdb; pdb.set_trace()
                if tokens[root_ind] > split_ind:
                    if nsubj_nmod_ind != 0 and cop_ind !=0:
                        _str1 = tokens[split_ind:cop_ind]
                    else:
                        _str1 = tokens[nsubj_ind+1:split_ind]
                    tokens[split_ind] = ''

                    if len(_str1) > 0 and (_str1[-1] in PUNCTUATION):
                        _str1[-1] = ''
                    if len(_str1) >0 and (_str1[0] in PUNCTUATION):
                        _str1[0] = ''

                    str1 = nsubj + " " + verb + ' '.join(_str1)

                    if nsubj_nmod_ind != 0 and cop_ind !=0:
                        _strs = tokens[cop_ind:]
                    else:
                        _strs = tokens[split_ind:]

                    _str2 = " ".join(_strs)
                    """
                    if len(person_taggers) > 0:
                        str2 = "He" + " " + ' '.join(_str2)  # 'he' will be replaced with 'he/she'

                    elif len(org_taggers) > 0:
                        if base.isplural(org_taggers[-1]):
                            str2 = "They" + " " + ' '.join(_str2)
                        else:
                            str2 = "It" + " " + ' '.join(_str2)
                    else:
                        str2 = nsubj + ' '.join(_str2)
                    """
                    nsubj = nsubj.strip()
                    _nsubj = nsubj[0].upper() + nsubj[1:]

                    if _nsubj == 'I' or _nsubj == 'He' or _nsubj == 'She':
                        str2 = _nsubj + _str2
                    else:
                        #sent2 = _nsubj + " " + _str2
                        #nsubj2 = base.replace_nsubj(sent2, nsubj)
                        #str2 = nsubj2 + _str2
                        str2 = _nsubj + " " + _str2

                else:

                    #import pdb; pdb.set_trace()
                    _str1 = tokens[nsubj_ind+1:root_ind]

                    if len(_str1) > 0 and _str1[-1] in PUNCTUATION:
                        _str1[-1] = ''
                    str1 = nsubj  + ' '.join(_str1)
                    #print "1st sent: ", str1

                    # upper the 1st char in 2nd sent
                    _strs = tokens[root_ind:]
                    _str2 = " ".join(_strs)
                    """
                    if len(person_taggers) > 0:
                        str2 = "He" + " " + ' '.join(_str2)  # 'he' will be replaced with 'he/she'

                    elif len(org_taggers) > 0:
                        if base.isplural(org_taggers.split()[-1]):
                            str2 = "They" + " " + ' '.join(_str2)
                        else:
                            str2 = "It" + " " + ' '.join(_str2)
                    else:
                        str2 = nsubj + ' '.join(_str2)
                    """
                    #w = _w + ' '
                    #str2 = nsubj  + ' '.join(_str2)
                    #print "2nd sent: ", str2
                    nsubj = nsubj.strip()
                    _nsubj = nsubj[0].upper() + nsubj[1:]

                    if _nsubj == 'I' or _nsubj == 'He' or _nsubj == 'She':
                        str2 = _nsubj + _str2
                    else:
                        #sent2 = _nsubj + " " + _str2
                        #nsubj2 = base.replace_nsubj(sent2, nsubj)
                        #str2 = nsubj2 + _str2
                        str2 = _nsubj + " " + _str2

                strs = str1 + ' . ' + str2

                #import pdb; pdb.set_trace()
                end_time = time.time()
                during_time = end_time - start_time
                print "The time of appos function: ", during_time

                return strs

            if auxpass_ind > 0:
                split_ind = 0
                if ',' in tokens:
                    split_ind = tokens.index(',')
                if split_ind == 0:
                    return strs

                #import pdb; pdb.set_trace()
                #verb = conjugate("be", tenses(root)[0][0], 3)
                verb = tokens[auxpass_ind]
                if tokens[root_ind] > split_ind:
                    _str1 = tokens[nsubj_ind+1:auxpass_ind]

                    if len(_str1) > 0 and _str1[-1] in PUNCTUATION:
                        _str1[-1] = ''
                    if len(_str1) > 0 and _str1[0] in PUNCTUATION:
                        _str1[0] = ''
                    str1 = nsubj  + " " + verb + ' '.join(_str1)
                    #print "1st sent: ", str1

                    # upper the 1st char in 2nd sent
                    _strs = tokens[auxpass_ind:]
                    _str2 = " ".join(_strs)

                    nsubj = nsubj.strip()
                    _nsubj = nsubj[0].upper() + nsubj[1:]

                    if _nsubj == 'I' or _nsubj == 'He' or _nsubj == 'She':
                        str2 = _nsubj + _str2
                    else:
                        #sent2 = _nsubj + " " + _str2
                        #nsubj2 = base.replace_nsubj(sent2, nsubj)
                        #str2 = nsubj2 + _str2
                        str2 = _nsubj + " " + _str2

                strs = str1 + ' . ' + str2

                return strs


    #import pdb; pdb.set_trace()
    end_time = time.time()
    during_time = end_time - start_time
    print "The time of appos function: ", during_time

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

    sent = "Peter, my son, ate an apple."
    sent = "Peter, my son, eats an apple."
    #sent = "Peter, my friend, likes it."
    sent = "Boys, my friends, like it."
    #sent = "City of Faizabad, the headquarters of Faizabad District, is a municipal board in the state of Uttar Pradesh , India ."
    #TODO: the tense of the output
    sent = "John Nash, a mathematician, lectured at Princeton."
    sent = "Boeing, the manufacturer of airplanes, is based in Seattle."
    sent = "Robert Downey Jr. , a mathematician, lectured at Princeton."
    sent = "Boeing, the airplane company, went bankrupt."
    #sent = "It is based in Seattle  ."
    print(simp_syn_sent_(sent))


if __name__ == '__main__':
    main()
