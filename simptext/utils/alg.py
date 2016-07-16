# -*- coding: utf-8 -*-
"""
  utils.alg
  ~~~~~~~~~~~
  syntacitc alg

@author wenlong
"""
# use the wrapper or use the standard lib?
from nltk.parse.stanford import StanfordDependencyParser

eng_parser = StanfordDependencyParser(model_path=u'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')

def split_sentence(sent):
    result = list(eng_parser.raw_parse(sent))[0]
    root = result.root['word']
    print "root: ", root

    """
    for node in result.nodes.items():
        print(node)
    """

    # Universal dependencies
    """ depes format, based on dependency graph in NLTK
    ((head word, head tag), rel, (dep word, dep tag))
    e.g.  ((u'ate', u'VBD'), u'nsubj', (u'I', u'PRP'))
    """
    depes = []
    for row in result.triples():
        print(row)
        depes.append(row)

        # look for the root word, and check the root word has a modifier
        if (root in row[0]) and (len(row[2]) != 0):
            # if "conj" relation, it is modified by row[2]
            if row[1] == 'conj': #

            elif row[1] == 'cc':
            else:

    # based on the splitting alg



#main
def main():
    sent = "I ate fish and he drank wine."
    res = split_sentence(sent)

if __name__ == '__main__':
    main()
