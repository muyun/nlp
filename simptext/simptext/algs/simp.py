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

from algs import punct, coordi, subordi, adverb, parti, adjec, appos, passive, paratax

import base

PUNCTUATION = (';', ':', ',', '.', '!', '?')
COMMA = ','

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

"""
def upper_first_char(w):
    return w[0].upper() + w[1:]
"""

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
    strs = coordi.simp_coordi_sent(tokens, node_list)
    #strs = simp_subordi_sent(tokens, node_list)
    #strs = simp_advcl_sent(tokens, node_list)
    #strs = simp_parti_sent(tokens, node_list)
    #strs = simp_adjec_sent(tokens, node_list)
    #strs = simp_appos_sent(tokens, node_list)
    #strs = simp_passive_sent(tokens, node_list)

    return strs

def simp_syn_sent(sent):
    strs = ""
    # the original tokens in the sent


    #import pdb; pdb.set_trace()
    #print "syn sent: ", sent
    #import pdb; pdb.set_trace()
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


    #import pdb; pdb.set_trace()
    if len(sent) > 0:
        strs = coordi.simp_coordi_sent(tokens, node_list)
        if len(strs) > 0:
            return strs
        else:
            strs = subordi.simp_subordi_sent(tokens, node_list)
            if len(strs) > 0:
                return strs
            else:
                strs = advcl.simp_subordi_sent(tokens, node_list)
                if len(strs) > 0:
                    return strs
                else:
                    strs = parti(tokens, node_list)
                    if len(strs) > 0:
                        return strs
                    else:
                        strs = adjec(tokens, node_list)
                        if len(strs) > 0:
                            return strs
                        else:
                            strs = appos(tokens, node_list)
                            if len(strs) > 0:
                                return strs
                            else:
                                strs = passive(tokens, node_list)
                                if len(strs) > 0:
                                    return strs


    return strs

#main
def main():
    # coordinated clauses
    sent = "He held it out, and with a delighted \"Oh!\""
    #sent = "I ate fish and he drank wine."
    sent = "We haven't totally forgotten about it, but we're looking forward to this upcoming season."
    sent = "I ate fish or he drank wine."

    sent = "I ate an apple and an orange."
    #print(simp_coordi_sent(sent))
    print(simp_syn_sent_(sent))

    # Subordinated Clauses and Adverbial Clauses
    sent= "Since he came, I left."
    sent = "Before he came, I left."
    #print(simp_subordi_sent(sent))
    #print(simp_syn_sent_(sent))

    # Adverbial Clauses
    sent = "Needing money, I begged my parents."
    #sent = "Ochoa's new teammates were generally pleased with the move, even if it wasn't a blockbuster."
    #sent = "I blinked when I opened the door."
    #print(simp_advcl_sent(sent))
    #print(simp_syn_sent(sent))

    # participial phrases
    sent = "Alicia, running down the street, tripped."
    #sent = "The MTR was immediately popular with residents of Hong Kong ; as a result , subsequent lines have been built to cover more territory . There are continual debates regarding how and where to expand the MTR network ."
    #print(simp_parti_sent(sent))
    #print(simp_syn_sent(sent))

    #Adjectival Clauses and Appositive phrases
    sent = "Peter, who liked fruits, ate an apple."
    #print(simp_adjec_sent(sent))
    #print(simp_syn_sent(sent))

    sent = "Peter, my son, ate an apple."
    #print(simp_appos_sent(sent))
    #print(simp_syn_sent(sent))

    sent = "Peter was hit by a bus."
    #print(simp_passive_sent(sent))
    sent = "Food is procured with its suckers and then crushed using its tough `` beak '' of chitin ."
    #print(simp_syn_sent_(sent))


if __name__ == '__main__':
    main()
