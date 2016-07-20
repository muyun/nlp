# -*- coding: utf-8 -*-
"""
  utils.alg
  ~~~~~~~~~~~
  syntacitc alg

@author wenlong
"""
import inspect

from nltk import Tree

# use the wrapper or use the standard lib?
from nltk.parse.stanford import StanfordDependencyParser

eng_parser = StanfordDependencyParser(model_path=u'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')


def simp_conj_sent(sent):
    result = list(eng_parser.raw_parse(sent))[0]
    root = result.root['word']
    #print "root: ", root

    words = []
    #import pdb; pdb.set_trace()
    for node in result.nodes.items():
        #print(node)
        #print(node[1]['word'])
        words.append(node[1]['word'])

    w = result.tree()
    #print "parse_tree:", w

    #TODO: use the tree, check again
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
    # construct the tree
    #partial = Tree(w[parent].label(), )
    _subtree = {}
    for subtree in w.subtrees():
        _subtree[subtree.label()] = subtree

    # store the subtree in the
    for nd in _subtree:
        childs = []
        for v in _subtree[nd]:
            if not isinstance(v, Tree):
                childs.append(v)
            #else:
            #    childs.append(v.label())
        _subtree[nd] = childs


    # Universal dependencies -- And relations
    """ depes format, based on dependency graph in NLTK
    ((head word, head tag), rel, (dep word, dep tag))
    e.g.  ((u'ate', u'VBD'), u'nsubj', (u'I', u'PRP'))
    """

    ret = []

    import pdb; pdb.set_trace()
    depes = []
    for row in result.triples():
        #print(row)
        depes.append(row)

        # look for the root word, and check the root word has a modifier
        if (root in row[0]) and (len(row[2]) != 0):
            # if "conj" relation, it is modified by row[2]
            if row[1] == 'conj': #

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

            elif row[1] == 'cc':

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

    # based on the splitting alg

    #import pdb; pdb.set_trace()
    #print

    #import pdb; pdb.set_trace()
    strs =""
    for str in ret:
        _strs = ' '.join(str)
        _strs = _strs + ' . '
        strs = strs + _strs

    return strs

def simp_advcl_sent(sent):
    result = list(eng_parser.raw_parse(sent))[0]
    root = result.root['word']
    #print "root: ", root

    words = []
    #import pdb; pdb.set_trace()
    for node in result.nodes.items():
        #print(node)
        #print(node[1]['word'])
        words.append(node[1]['word'])

    w = result.tree()
    #print "parse_tree:", w

    #TODO: should use the tree struture, check again
    # construct the tree
    #partial = Tree(w[parent].label(), )
    _subtree = {}
    for subtree in w.subtrees():
        _subtree[subtree.label()] = subtree

    # store the subtree in the

    import pdb; pdb.set_trace()
    for nd in _subtree:
        childs = []
        for v in _subtree[nd]:
            if not isinstance(v, Tree):
                childs.append(v)
            #else:
            #    childs.append(v.label())
        _subtree[nd] = childs


    # Universal dependencies -- And relations
    """ depes format, based on dependency graph in NLTK
    ((head word, head tag), rel, (dep word, dep tag))
    e.g.  ((u'ate', u'VBD'), u'nsubj', (u'I', u'PRP'))
    """

    ret = []

    import pdb; pdb.set_trace()
    depes = []
    for row in result.triples():
        #print(row)
        depes.append(row)

        # look for the root word, and check the root word has a modifier
        if (root in row[0]) and (len(row[2]) != 0):
            # if "advcl" relation, it is modified by row[2]
            if row[1] == 'advcl': #
                print "advcl_node: ", _subtree[row[2][0]]

                # check whether 'mark' modifier
                for _row in result.triples():
                    # if the "advcl" modifier has a "mark" modifier that is either "since" or "because" (yes)
                    if (row[2] == _row[0]) and (_row[1] == 'mark'):
                        print "mark modifier: ", row
                        # remove the 'advcl' modifier



                #
                lst = []
                lst.append(row[2][0])
                for k in _subtree[row[2][0]]:
                    lst.append(k)
                #lst.append(row[2][0])

                lst_ = sorted(lst, key=lambda x: words.index(x))
                #print "conj_lst_: ", lst_
                ret.append(lst_)


            else:
                #print "Hello, World"
                pass

    # based on the splitting alg

    #import pdb; pdb.set_trace()
    #print

    #import pdb; pdb.set_trace()
    strs =""
    for str in ret:
        _strs = ' '.join(str)
        _strs = _strs + ' . '
        strs = strs + _strs

    return strs


#main
def main():
    #sent = "I ate fish and he drank wine."
    #sent = "he likes swimming and I like football."
    #sent = "I like swimming and he love running and she likes badminton"
    #sent = " Her wrist, when I grabbed it, was smooth and strong and warm in my fingers."
    sent = "Integra-A Hotel &amp; Restaurant Co. said its planned rights offering to raise about $9 million was declared effective and the company will begin mailing materials to shareholders at the end of this week."
    res = simp_conj_sent(sent)
    print(res)

    """
    sent= "Since/Because he came, I left."
    res = simp_advcl_sent(sent)
    """

if __name__ == '__main__':
    main()
