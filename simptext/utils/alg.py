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

import base

PUNCTUATION = (';', ':', ',', '.', '!', '?')

def traverse(t):
    try:
        t.label()
    except AttributeError:
        print(t + " ")
    else:
        # Now we know that t.node is defined

        #import pdb; pdb.set_trace()
        print('(', t.label())
        for child in t:
            traverse(child)
        print(')')

def upper_first_char(w):
    return w[0].upper() + w[1:]

def simp_coordi_sent(sent):
    tokens = StanfordTokenizer().tokenize(sent)
    tokens.insert(0, '')

    result = list(eng_parser.raw_parse(sent))[0]
    root = result.root['word']


    node_list = [] #(4, u'said', u'VBD', u'root', [[18], [22], [16], [3]])
    for node in result.nodes.items():
        #print(node)
        node_list.append(base.get_triples(node))

    """
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
        if (root in nd) and ('cc' in nd[4].keys()) and ('conj' in nd[4].keys()):
              # coordination
            # Note: remove the conjunction word, and
            #       if there is words before the conjunction, we consider it as a sent,
            #       or,
            #import pdb; pdb.set_trace()
            #print "cc_node: ", nd[4]['cc']
            cc_ind = nd[4]['cc'][0]

            # remove the conjunction word

            #import pdb; pdb.set_trace()
            tokens[cc_ind] = ''
            if tokens[cc_ind - 1] == '':# no word before the conjunction word
                pass
            elif tokens[cc_ind - 1] in PUNCTUATION:
                tokens[cc_ind - 1] = ''
                tokens[cc_ind] = '.'
            else:# we can add ' . ' as the end of the 1st sentence
                tokens[cc_ind] = '. '

            #NOTE: We can consider the next word after the conjunction as the first word of 2nd sentence
            word = tokens[cc_ind + 1]
            tokens[cc_ind + 1] = upper_first_char(word)

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
            strs = ' '.join(tokens)
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


def simp_subordi_sent(sent):
    PUNCT = ','
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

    # the original tokens in the sent
    tokens = StanfordTokenizer().tokenize(sent)
    tokens.insert(0, '')

    result = list(eng_parser.raw_parse(sent))[0]
    root = result.root['word']

    #w = result.tree()
    #print "parse_tree:", w

    #TODO: use the tree structure, check again
    """
    _tree = {} # store the _tree-> {node: children}
    #import pdb; pdb.set_trace()
    for postn in w.treepositions():
        if w.label() and len(postn) > 0:
            parent = postn[:-1]

            nd = w[parent].label() #node
            if nd in _tree:
                _tree[nd].append(w[postn])
            else:
                _tree[nd] = []
                _tree[nd].append(w[postn])

    """

    # Universal dependencies --
    """ depes format, based on dependency graph in NLTK
    ((head word, head tag), rel, (dep word, dep tag))
    e.g.  ((u'ate', u'VBD'), u'nsubj', (u'I', u'PRP'))
    """
    node_list = [] # dict (4 -> 4, u'said', u'VBD', u'root', [[18], [22], [16], [3]])
    for node in result.nodes.items():
        #print(node)
        node_list.append(base.get_triples(node))
        #node_list[base.get_triples[0]] = base.get_triples(node)

    # construct the tree
    #partial = Tree(w[parent].label(), )
    """
     # store the subtree in the
    for nd in _subtree:
        childs = []
        for v in _subtree[nd]:
            if not isinstance(v, Tree):
                childs.append(v)
            #else:
            #    childs.append(v.label())
        _subtree[nd] = childs
    """

    strs = ""
    split_ind = 0
    mark_ind = 0
    for nd in node_list[1:]:
        import pdb; pdb.set_trace()
        #print(nd)
        if (root in nd) and ('advcl' in nd[4].keys()):
            #print "conj: ", nd
            #print "conj node: ", nd[4]['conj']
            pass

        if (root in nd) and ('advcl' in nd[4].keys()):
            advcl_ind = nd[4]['advcl'][0]
            advcl_dic = node_list[advcl_ind][4]

            if ('mark' in advcl_dic.keys()):
                import pdb; pdb.set_trace()
                mark_ind = node_list[advcl_ind]['mark'][0]

                # get the marker,  delete the conjunction
                tokens[mark_ind] = ''
                tokens[mark_ind+1] = upper_first_char(tokens[mark_ind+1])
                # if the marker is in the dict1
                # [NOTICE]: we use the punctuation to check the sentence
                if (tokens[mark_ind].lower() in dict1.keys()): # if dict1, subordinated clause goes first
                    # delete the conjunction,
                    #tokens[mark_ind] = ''
                    #tokens[mark_ind+1] = upper_first_char(tokens[mark_ind+1])

                    #[NOTICE]: we consider 1st ',' to split the sentence, and get the 2nd sentence
                    if PUNCT in tokens:
                        split_ind = tokens.index(PUNCT)
                        tokens[split_ind] = ''
                         #import pdb; pdb.set_trace()
                        #print "tokens: ", tokens[split_ind+1]
                        #= tokens[split_ind+1][0].upper() + tokens[split_ind+1][1:]
                        _str1 = tokens[:(split_ind)]
                        str1 = ' '.join(_str1)
                        #print "1st sent: ", str1

                        _str2 = tokens[(split_ind+1):]
                        w = dict1[tokens[mark_ind].lower()] + ' '
                        str2 = w  + ' '.join(_str2)
                        #print "2nd sent: ", str2

                        strs = str1 + ' . ' + str2

                        return strs

                # if dict2, the subordinated clause goes second
                if (tokens[mark_ind].lower() in dict2.keys()):
                    if PUNCT in tokens:
                        split_ind = tokens.index(PUNCT)
                        _str1 = tokens[:(split_ind)]
                        str1 = ' '.join(_str1)
                        #print "1st sent: ", str1

                        _str2 = tokens[(split_ind+1):]
                        w = dict2[tokens[mark_ind].lower()] + ' '
                        str2 = w  + ' '.join(_str2)
                        #print "2nd sent: ", str2

                        strs = str1 + ' . ' + str2
                        return strs


        #if mark_ind == 0:  # if no mark word
        # adverbial clauses [NOTICE]: consider ',' to split the sentence


    return strs


#main
def main():
    # coordinated clauses

    sent = "He likes swimming and I like football."
    #sent = "I like swimming and he love running and she likes badminton"

    #sent = "Integra-A Hotel  Co. said its planned rights offering to raise about $9 million was declared effective and the company will begin mailing materials to shareholders at the end of this week."

    sent = "He held it out, and with a delighted \"Oh!\""
    sent = "and this is factory is critical to meeting that growing demand."
    sent = "He looked me and at last said, \"Very well.\""
    sent = "For information on COPIA events open to the public, sign on to www.copia.org"
    sent = "I ate fish and he drank wine"
    #sent = "I ate fish and he drank wine."
    sent = "We haven't totally forgotten about it, but we're looking forward to this upcoming season."
    sent = "By contrast, European firms will spend $150 million this year on electronic security, and are expected to spend $1 billion by 1992."
    #print(simp_coordi_sent(sent))


    # Subordinated Clauses and Adverbial Clauses
    sent= "Since he came, I left."
    #sent = " Since he took the head coaching job at bottom-dwelling Vanderbilt, the question Bobby Johnson is asked most often is not, &quot;Why will things be different under you?"
    #sent = "Because he took the head, the question is asked?"
    #sent = "A mission to end a war"
    sent = "Before he came, I left."
    sent = "If IBM has miscalculated the demand, it will suffer badly as both the high operating costs and depreciation on the huge capital investment for the East Fishkill factory drag down earnings."
    sent = "The black door opened as we came up to it, and a pale man opened the door."
    sent = "If we only had a human on our staff, we could have done so ages ago and sold it off, but we have no such luck."
    sent = "Tokhtakhounov's action apparently came soon after he said he received a phone call from the mother of the female ice dancer, presumably Anissina."
    sent = "As reinstalled in Washington, the kitchen should be as we all remember it from countless TV shows, \"right down to the toothpicks.\""
    sent = "he version endorsed by the APA would license doctoral-level psychologists to independently prescribe psychotropic drugs after completing 300 hours of classroom instruction in neuroscience, physiology and pharmacology, followed by four months' supervised treatment of 100 patients."

    sent = "The black door opened as we came up to it, and a pale man opened the door."
    sent = "\“As if I wanted it,\” interrupted the woman."
    sent = "If we only had a human on our staff, we could have done so ages ago and sold it off, but we have no such luck."
    sent = "If IBM has miscalculated the demand, it will suffer badly as both the high operating costs and depreciation on the huge capital investment for the East Fishkill factory drag down earnings."
    sent= "Since he came, I left."
    print(simp_subordi_sent(sent))


    # Adverbial Clauses
    #sent = "Needing money, I begged my parents."
    #print(simp_advcl_sent(sent))

    # Appositive phrase

    # Adjectival Clauses and Appositive phrases


if __name__ == '__main__':
    main()
