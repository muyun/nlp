# -*- coding: utf-8 -*-
"""
  utils.alg
  ~~~~~~~~~~~
  syntacitc algs

@author wenlong
"""
import inspect

from nltk import Tree
from nltk.tree import *

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

PUNCTUATION = (';', ':', ',', '.', '!', '?')
COMMA = ','

def simp_relcl_sent(tokens, node_list):
    strs = ""
    
    root_ind = node_list[0][4]['root'][0]
    root = tokens[root_ind]
    
    nsubj = ""
    nsubj_ind = 0
    for nd in node_list[1:]:
        if (root in nd) and ('nsubj' in nd[4].keys()):
            nsubj_ind = nd[4]['nsubj'][0]
            
    #import pdb; pdb.set_trace()
    verb_ind = 0
    for nd in node_list[1:]:
        #import pdb; pdb.set_trace()
        if (nsubj_ind == nd[0]) and ('acl:relcl' in nd[4].keys()):
            #import pdb; pdb.set_trace()
            #nsubj_ind = nd[4]['nsubj'][0]
            verb_ind =  nd[4]['acl:relcl'][0]
            
            nsubj_dict = {}
            nsubj_compound_list = []
            amod_list = []
            det_ind = 0
            
            for _nd in node_list:
                if (nsubj_ind == _nd[0]):
                    nsubj_dict = _nd[4]
                if ('amod' in nsubj_dict.keys()):
                    amod_list = nsubj_dict['amod']
                if ('compound' in nsubj_dict.keys()):
                    nsubj_compound_list = nsubj_dict['compound']
                if ('det' in nsubj_dict.keys()):
                    det_ind = nsubj_dict['det'][0]
                    #break

            for j in amod_list:
                nsubj = nsubj + " " + tokens[j]
            for i in nsubj_compound_list:
                nsubj = nsubj + " " + tokens[i]
            if det_ind > 0:
                nsubj = tokens[det_ind] + " " + nsubj + " " + tokens[nsubj_ind]
            else:
                nsubj = nsubj + " " + tokens[nsubj_ind]

            _nsubj = nsubj[0].upper() + nsubj[1:]
            nsubj = _nsubj.strip()  + " "


            import pdb; pdb.set_trace()
            split_ind = 0
            if COMMA in tokens:
                split_ind = tokens.index(COMMA)

            if split_ind < verb_ind:
                _strs = tokens[verb_ind:root_ind]
                if _strs[-1] in PUNCTUATION:
                    _strs.pop(-1)

                _str1 = ' '.join(_strs) + " . "
                str1 = nsubj + _str1

                _str2 = " ".join(tokens[root_ind:])
                if nsubj == 'I' or nsubj == 'He' or nsubj == 'She':
                    str2 = nsubj + _str2
                else:
                    #sent2 = nsubj + " " + _str2
                    #nsubj2 = base.replace_nsubj(sent2, nsubj)
                    #str2 = nsubj2 + _str2
                    str2 = nsubj + " " + _str2

                strs = str1 + str2
            
            else:
                _str1 = tokens[:nsubj_ind+1]
                str1 = ' '.join(_str1) + " . "

                _strs = tokens[nsubj_ind+1:]
                if _strs[0] in PUNCTUATION:
                    _strs.pop(0)
                if ('which' in _strs[0]) or ('who' in _strs[0]):
                    _strs.pop(0)

                _str2 = " ".join(_strs)

                if _nsubj == 'I' or _nsubj == 'He' or _nsubj == 'She':
                    str2 = _nsubj + _str2
                else:
                    #sent2 = _nsubj + " " + _str2
                    #nsubj2 = base.replace_nsubj(sent2, nsubj)
                    #str2 = nsubj2 + _str2
                    str2 = _nsubj + " " + _str2

    #str2 = base.replace_nsubj(tokens, nsubj) +  ' '.join(_str2)

                strs = str1 + str2
    """
    stree = [parse.tree() for parse in eng_parser.raw_parse(sent)][0]

    #import pdb; pdb.set_trace()
    for postn in stree.treepositions():
        if stree.label().endswith("=H"):
            parentpos = postn[:-1]
            partial = Tree(stree[parentpos].label(), [ stree[postn] ])
    """

    #import pdb; pdb.set_trace()
    #strs = simp_relcl_sent(result)

    """
    lst = []
    se = 0
    head = ""
    dependent = ""
    for nd in re:
        if 'nsubj' in nd[1] or 'nsubjpass' in nd[1]:
            head = nd[0][0]
            dependent = nd[2][0]
    """

    #for node in node_list[1:]:

    return strs

def simp_syn_sent_(sent):
    strs = ""
    #print(sent)
    #import pdb; pdb.set_trace()
    tokens = StanfordTokenizer().tokenize(str(sent))
    #tokens = wordpunct_tokenize(str(sent))
    tokens.insert(0, '')

    re = list(eng_parser.raw_parse(sent))[0]
    root = re.root['word']

    node_list = [] # dict (4 -> 4, u'said', u'VBD', u'root', [[18], [22], [16], [3]])
    for node in re.nodes.items():
        node_list.append(base.get_triples(node))

    #result = list(eng_parser.raw_parse(sent))[0]
    #root = result.root['word']

    strs = simp_relcl_sent(tokens, node_list)

    return strs


def main():
    # adjectival Clauses
    sent = "Dodd simply retained his athletic director position , which he had acquired in 1950 ."
    sent = "At present it is formed by the Aa , which descends from the Rigi and enters the southern extremity of the lake ."
    sent = "Phosgene can be detected at 0.4 ppm , which is four times the Threshold Limit Value ."
    sent = "Slaves were previously introduced by the British and French who colonized the island in the 18th century ."
    sent = "Fernando Navarro i Corbacho is a Spanish footballer who currently plays for Sevilla FC , as a left defender ."
    sent = "The city was first founded by the British in 1827 , who leased the island from Spain during the colonial period ."

    sent = "Slaves were previously introduced by the British and French who colonized the island in the 18th century ."
    sent = "Typically , the biggest difference between film and stage musicals is the use of lavish background scenery which would be impractical in a theater ."
    #sent = "Fernando Navarro i Corbacho is a Spanish footballer who currently plays for Sevilla FC , as a left defender ."
    sent = "Peter, who liked fruits, ate an apple."
    sent = "They renamed the place Alcante or Alcanatif which means Port of Salt , due to the old salt industry of Phoenicians and Romans ."
    #print(simp_coordi_sent(sent))
    print(simp_syn_sent_(sent))


if __name__ == '__main__':
    main()
