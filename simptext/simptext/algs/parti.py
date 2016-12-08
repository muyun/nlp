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

from pattern.en import tenses, conjugate

#from algs import base
import base
#import time

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
        if (root in nd) and ('nsubj' in nd[4].keys()):
            pass

        if (root in nd) and ('nsubj' in nd[4].keys()):
            #print "conj: ", nd
            #print "conj node: ", nd[4]['conj']

            #import pdb; pdb.set_trace()
            nsubj_ind = nd[4]['nsubj'][0]
            nsubj_dict = {}
            nsubj_compound_list = []
            for _nd in node_list: #BUG
                if nsubj_ind == _nd[0]:
                     nsubj_dict = _nd[4]
                     if ('compound' in nsubj_dict.keys()):
                         nsubj_compound_list = nsubj_dict['compound']
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

                #subj = tokens[nsubj_ind]
                #import pdb; pdb.set_trace()
                nsubj = ""
                for i in nsubj_compound_list:
                    nsubj = nsubj + " " + tokens[i]
                nsubj = nsubj + " " + tokens[nsubj_ind]
                nsubj = nsubj[0].upper() + nsubj[1:] + " "
                #tokens.insert(1, upper_first_char(subj))

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
                #verb = "be"
                verb = conjugate("be", tenses(root)[0][0], 3)
                root_ind = tokens.index(root)

                advmod_ind = 0
                for _nd in node_list[1:]:
                    if acl_ind == _nd[0]:
                        acl_dict = _nd[4]
                        break
                if ('advmod' in acl_dict.keys()):
                    advmod_ind = acl_dict['advmod'][0]

                if advmod_ind == 0:
                    _str1 = tokens[acl_ind:root_ind]
                else:
                    _str1 = tokens[advmod_ind:root_ind]

                if len(_str1) > 0 and _str1[-1] in PUNCTUATION:
                    _str1[-1] = ''

                #str1 = base.upper_first_char(nsubj) + " " + verb + " "
                str1 = nsubj + " " + verb + " "
                str1 =  str1 + ' '.join(_str1)
                #print "1st sent: ", str1

                # upper the 1st char in 2nd sent

                #import pdb; pdb.set_trace()
                _strs = tokens[root_ind:]
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
                    sent2 = _nsubj + " " + _str2
                    nsubj2 = base.replace_nsubj(sent2, nsubj)
                    str2 = nsubj2 + _str2
                #w = _w + ' '
                #str2 = base.upper_first_char(nsubj) + " " + ' '.join(_str2)
                #print "2nd sent: ", str2

                strs = str1 + ' . ' + str2
                #return strs

            #if ('acl' in nsubj_dict.keys()):


    #end_time = time.time()
    #during_time = end_time - start_time
    #print "The time of parti function: ", during_time
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
    strs = simp_parti_sent(tokens, node_list)
    #strs = simp_adjec_sent(tokens, node_list)
    #strs = simp_appos_sent(tokens, node_list)
    #strs = simp_passive_sent(tokens, node_list)

    return strs


def main():
    # participial clauses
    sent = "Alicia, running down the street, tripped."

    sent = "Peter, also called Pete, came."

    #sent = "The MTR was immediately popular with residents of Hong Kong ; as a result , subsequent lines have been built to cover more territory . There are continual debates regarding how and where to expand the MTR network ."

    #sent = "Radiometric dating is a technique used to date materials , usually based on a comparison between the observed abundance of a naturally occurring radioactive isotope and its decay products , using known decay rates ."

    sent = "John Nash, running down the street, tripped."
    #sent = "Port Arthur was also the destination for juvenile convicts , receiving many boys , some as young as nine arrested for stealing toys ."
    sent = "Alicia, running down the street, tripped."
    sent = "Peter, also called Pete, came."
    sent = "Peter, sweating hard, arrived."
    #print(simp_coordi_sent(sent))
    print(simp_syn_sent_(sent))


if __name__ == '__main__':
    main()
