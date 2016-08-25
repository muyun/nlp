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

#from alg import base
import base

PUNCTUATION = (';', ':', ',', '.', '!', '?')

def connect_sent(conj_ind, tokens, node_list):
    #
    _strs = ""
    another_cc_ind = 0
    another_conj_ind = 0
    
    _cc_ind = 0
    _conj_ind = 0
    nsubj_ind = 0
    for _nd in node_list[1:]:
        if conj_ind == _nd[0]: 
            if ('conj' in _nd[4].keys()) and ('cc' in _nd[4].keys()):
                _conj_ind = _nd[4]['conj'][0]
                _cc_ind = _nd[4]['cc'][0]
                
    for _nd in node_list[1:]:
        if _conj_ind == _nd[0]:
            if ('nsubj' in _nd[4].keys()):
                nsubj_ind = _nd[4]['nsubj'][0]

            if ('conj' in _nd[4].keys() and ('cc' in _nd[4].keys())):
                another_cc_ind = _nd[4]['cc'][0]
                another_conj_ind = _nd[4]['conj'][0]    
                
    #import pdb; pdb.set_trace()
    nsubj = ' '
    tokens[_cc_ind] = ''
    #if tokens[_cc_ind - 1] == '':  # no word before the conjunction word
    #    pass
    if tokens[_cc_ind - 1] in PUNCTUATION:
        tokens[_cc_ind - 1] = ''
        tokens[_cc_ind] = '.'
    if tokens[_cc_ind + 1] in PUNCTUATION:
        tokens[_cc_ind + 1] = ''
    
    nsubj = base.upper_first_char(tokens[nsubj_ind]) + nsubj
    
    if (another_cc_ind != 0) and (another_conj_ind != 0):  # one more cc
        _str2 = connect_sent(_conj_ind, tokens[another_cc_ind:], node_list)
        _strs = nsubj + " ".join(tokens[(nsubj_ind+1):]) + " . " + _str2
        
    else:
        _strs = nsubj + " ".join(tokens[(nsubj_ind+1):])
        
    return _strs

        
def simp_coordi_sent(tokens, node_list):
    """
    tokens = StanfordTokenizer().tokenize(sent)
    tokens.insert(0, '')

    result = list(eng_parser.raw_parse(sent))[0]
    root = result.root['word']


    node_list = [] #(4, u'said', u'VBD', u'root', [[18], [22], [16], [3]])
    for node in result.nodes.items():
        #print(node)
        node_list.append(base.get_triples(node))

    # construct the tree
    #w = result.tree()
    #partial = Tree(w[parent].label(), )
    _subtree = {}
    for subtree in w.subtrees():
        #import pdb; pdb.set_trace()
        #traverse(subtree)
        _subtree[subtree.label()] = subtree

    """

    # Universal dependencies -- And relations
    """ depes format, based on dependency graph in NLTK
    ((head word, head tag), rel, (dep word, dep tag))
    e.g.  ((u'ate', u'VBD'), u'nsubj', (u'I', u'PRP'))
    ##### node_list
    e.g. #(4, u'said', u'VBD', u'root', [[18], [22], [16], [3]])
    """
    root = ""
    root_ind = node_list[0][4]['root'][0]
    for nd in node_list:
        if root_ind == nd[0]:
            root=nd[1]

    #import pdb; pdb.set_trace()

    strs = ""
    for nd in node_list[1:]:
        #print(nd)
        #depes.append(row)

        #import pdb; pdb.set_trace()
        # look for the root word, and check the root word has a modifier
        """
        #if (root in nd) and ('conj' in nd[4].keys()):
            # if "conj" relation, it is modified by row[2]
            #import pdb; pdb.set_trace()
            #print "conj_node: ", nd[4]['conj']
        #    pass
            #

            lst = []
            lst.append(row[2][0])
            if row[2][0] in _subtree:
                #print "conj_node: ", _subtree[row[2][0]]
                for k in _subtree[row[2][0]]:
                    lst.append(k)
            #lst.append(row[2][0])

            lst_ = sorted(lst, key=lambda x: tokens.index(x))
            #print "conj_lst_: ", lst_
            ret.append(lst_)
        """
        if (root in nd) and ('conj' in nd[4].keys()) and ('cc' in nd[4].keys()):
            # coordination
            # Note: remove the conjunction word, and
            #       if there is words before the conjunction, we consider it as a sent,
            #       or,
            #import pdb; pdb.set_trace()

            nsubj = " "
            nsubj_ind = 0
            FLAG = 0

            # one more cc?
            another_cc_ind = 0
            another_conj_ind = 0
            
            #Assume the nsubj is the before word of the conj_ind
            conj_ind = nd[4]['conj'][0]
            conj_nsubj_ind = 0
            for _nd in node_list[1:]:
                if conj_ind == _nd[0]: # the first cc
                    if ('nsubj' in _nd[4].keys()) or ('nsubjpass' in _nd[4].keys()):
                        # another subj :THE ASSUME
                        #nsubj_ind = conj_ind - 1
                        conj_nsubj_ind = _nd[4]['nsubj'][0]
                        conj_nsubj = base.upper_first_char(tokens[conj_nsubj_ind]) + nsubj
                        FLAG = 1 # use the subj
                        
                        #break
                    # there is one more cc    
                    if ('conj' in _nd[4].keys() and ('cc' in _nd[4].keys())):
                        another_cc_ind = _nd[4]['cc'][0]
                        another_conj_ind = _nd[4]['conj'][0]
                        
                    break        

            # get nsubj
            #nsubj = " "
            if ('nsubj' in nd[4].keys()):
                nsubj_ind = nd[4]['nsubj'][0]
                nsubj =  base.upper_first_char(tokens[nsubj_ind]) + nsubj

            if ('nsubjpass' in nd[4].keys()):
                nsubj_ind = nd[4]['nsubjpass'][0]
                nsubj = base.upper_first_char(tokens[nsubj_ind]) + nsubj

            #print "cc_node: ", nd[4]['cc']
            cc_ind = nd[4]['cc'][0]

            # 1st str1
            # remove the conjunction word

            #import pdb; pdb.set_trace()
            tokens[cc_ind] = ''
            if tokens[cc_ind - 1] == '':  # no word before the conjunction word
                pass
            elif tokens[cc_ind - 1] in PUNCTUATION:
                tokens[cc_ind - 1] = ''
                tokens[cc_ind] = '.'
            elif tokens[cc_ind + 1] in PUNCTUATION:
                tokens[cc_ind + 1] = ''
            else:# we can add ' . ' as the end of the 1st sentence
                tokens[cc_ind] = '.'

            str1 = nsubj + " ".join(tokens[(nsubj_ind+1):(cc_ind+1)])

            #NOTICE: We can consider the next word after the conjunction as the first word of 2nd sentence
            # str2
            
            #NOTICE: one more cc?

            #import pdb; pdb.set_trace()
            """
            if (another_cc_ind != 0) and (another_conj_ind != 0):  # one more cc
                _str2 = connect_sent(conj_ind, tokens, node_list)
                if FLAG:
                    #str2 =  nsubj + " ".join(tokens[(cc_ind+1):another_cc_ind]) + " . " + _str2
                    str2 =  conj_nsubj + " ".join(tokens[(conj_nsubj_ind+1):another_cc_ind]) + " . " + _str2
            """       
            
            if not FLAG:
                str2 = nsubj + " ".join(tokens[(cc_ind + 1):])
            else:
                str2 = conj_nsubj + " ".join(tokens[(conj_nsubj_ind + 1):])
                
            """
            lst = []
            lst.append(row[0][0])
            if row[0][0] in _subtree:
                #print "cc_node: ", _subtree[row[0][0]]
                for k in _subtree[row[0][0]]:
                    # remove the 'cc' modifier
                    if k == row[2][0]:
                        pass
                    else:
                        lst.append(k)
            #lst.append(row[0][0])

            lst_ = sorted(lst, key=lambda x: tokens.index(x))
            print "cc_lst_: ", lst_
            #ret.append(lst_)
            """
            strs = str1 + " " + str2
            
            return strs
        
        elif (root in nd) and ('dobj' in nd[4].keys() or 'nsubj' in nd[4].keys()):
            #

            #import pdb; pdb.set_trace()
            cc_ind = 0
            dobj_ind = 0
            if ('dobj' in nd[4].keys()):
                dobj_ind = nd[4]['dobj'][0]
                for _nd in node_list[1:]:
                    if (dobj_ind == _nd[0]) and ('conj' in _nd[4].keys()) and ('cc' in _nd[4].keys()):
                        cc_ind = _nd[4]['cc'][0]
                        break

            nsubj_ind = 0
            if ('nsubj' in nd[4].keys()): # there is BUG here
                nsubj_ind = nd[4]['nsubj'][0]
                for _nd in node_list[1:]:
                    if (nsubj_ind == _nd[0]) and ('conj' in _nd[4].keys()) and ('cc' in _nd[4].keys()):
                        cc_ind = _nd[4]['cc'][0]
                        break

            #import pdb; pdb.set_trace()
            str1 = " ".join(tokens[:(dobj_ind+1)])
            str2 = " ".join(tokens[:(root_ind+1)] + tokens[cc_ind+1:])

            if str1:
                return strs
            if str2:
                return strs 
            else:  
                strs = str1 + " . " + str2

            return strs

        else:
            #print "Hello, World"
            pass

    """
    ret = []

    depes = []
    for row in result.triples():
        #print(row)
        depes.append(row)

        #import pdb; pdb.set_trace()
        # look for the root word, and check the root word has a modifier
        if (root in row[0]) and (len(row[2]) != 0) and (row[1] == 'conj'):
            # if "conj" relation, it is modified by row[2]
            #import pdb; pdb.set_trace()
            #print "conj_node: ", _subtree[row[2][0]]
            #
            lst = []
            lst.append(row[2][0])
            if row[2][0] in _subtree:
                #print "conj_node: ", _subtree[row[2][0]]
                for k in _subtree[row[2][0]]:
                    lst.append(k)
            #lst.append(row[2][0])

            lst_ = sorted(lst, key=lambda x: words.index(x))
            #print "conj_lst_: ", lst_
            ret.append(lst_)

        elif (root in row[0]) and (len(row[2] != 0)) and (row[1] == 'cc'):

            #import pdb; pdb.set_trace()
            #print "cc_node: ", _subtree[row[0][0]]
            lst = []
            lst.append(row[0][0])
            if row[0][0] in _subtree:
                #print "cc_node: ", _subtree[row[0][0]]
                for k in _subtree[row[0][0]]:
                    # remove the 'cc' modifier
                    if k == row[2][0]:
                        pass
                    else:
                        lst.append(k)
            #lst.append(row[0][0])

            lst_ = sorted(lst, key=lambda x: words.index(x))
            #print "cc_lst_: ", lst_
            ret.append(lst_)
        else:
            #print "Hello, World"
            pass

    """

    #import pdb; pdb.set_trace()

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
    strs = simp_coordi_sent(tokens, node_list)
    #strs = simp_subordi_sent(tokens, node_list)
    #strs = simp_advcl_sent(tokens, node_list)
    #strs = simp_parti_sent(tokens, node_list)
    #strs = simp_adjec_sent(tokens, node_list)
    #strs = simp_appos_sent(tokens, node_list)
    #strs = simp_passive_sent(tokens, node_list)

    return strs

def main():
    # coordinated clauses
    sent = "He held it out, and with a delighted \"Oh!\""
    #sent = "I ate fish and he drank wine."
    sent = "We haven't totally forgotten about it, but we're looking forward to this upcoming season."
    sent = "I ate fish or he drank wine."

    #sent = "I ate an apple and an orange."
    sent = "I ate an apple and an orange."
    sent = "He is an actor and a musician."
    sent = "I ate fish and he drank wine and she ate fish."
    sent = "I am a student and he is a teacher and she is a doctor."
    sent = "I am a student and he is a teacher and she is a doctor and he is a farmer."
    #sent = "I am a student and he is a teacher ."
    #print(simp_coordi_sent(sent))
    print(simp_syn_sent_(sent))    

        
if __name__ == '__main__':
    main()
