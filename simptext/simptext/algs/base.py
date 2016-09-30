# -*- coding: utf-8 -*-
"""
   utils.base
   ~~~~~~~~~~
   base common function
"""
from itertools import chain
from collections import defaultdict

"""
from nltk.parse.stanford import StanfordDependencyParser
eng_parser = StanfordDependencyParser(model_path=u'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')
"""
#import en_nb

"""
nodes = defaultdict(lambda:  {'address': None,
                                    'word': None,
                                    'lemma': None,
                                    'ctag': None,
                                     'tag': None,
                                    'feats': None,
                                    'head': None,
                                     'deps': defaultdict(list),
                                     'rel': None,
                                         })
root = None
"""

verb_map = {
    "3rd singular present": "3rd"
}

def isplural(w):
        word = w.lower()
        lemma = lmtzr.lemmatize(word, 'n')
        plural = True if word is not lemma else False
        return plural

def upper_first_char(w):
    if len(w) > 1:
        return w[0].upper() + w[1:] 
    elif len(w) == 1:
        return w[0].upper() 
    else:
        return ""              


def get_triples(node):
    """
    Extract dependency triples of the form:
    (32, u'week', u'NN', u'nmod', defaultdict(<type 'list'>, {u'case': [30], u'det': [31]}))
    """

    #import pdb; pdb.set_trace()
    return (node[1]['address'], node[1]['word'], node[1]['ctag'], node[1]['rel'], node[1]['deps'])      

    """
    head = (node['word'], node['ctag'])

    import pdb; pdb.set_trace()
    for i in sorted(chain.from_iterable(node['deps'].values())):
        dep = get_by_address(i)
        yield (head, dep['rel'], (dep['word'], dep['ctag']))
        for triple in triples(node=dep):
            yield triple
    """


def update_vb_conjugation(v, v1):
    """ update the verb conjugation of v based on v1's tense """

    #import pdb; pdb.set_trace()
    _v1 = ""
    _v1 = en_nb.verb.tense(v1)
    _v = en_nb.verb.present(v, person=verb_map[_v1])

    return _v
  

def main():
        sent = "Integra-A Hotel  Co. said its planned rights offering to raise about $9 million was declared effective and the company will begin mailing materials to shareholders at the end of this week."

        """
        result = list(eng_parser.raw_parse(sent))[0]
        #print(result)
        #re = triples(result)

        triples = []
        
        for node in result.nodes.items():
            #import pdb; pdb.set_trace()
            print(node)
            
            triples.append(get_triples(node))
            
        #print(node[1]['word'])
            #print(node[1]['word'])
            #print(node)

        
        for row in result:
            print(row)
            print(row['word'] + ":" + row['address'] )
        
        """
        
        v = update_vb_conjugation('be', 'likes')

        
if __name__ == '__main__':
        main()

        
