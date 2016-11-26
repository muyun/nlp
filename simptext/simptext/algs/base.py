# -*- coding: utf-8 -*-
"""
   utils.base
   ~~~~~~~~~~
   base common function
   define some linguistics rules
"""
from itertools import chain
from collections import defaultdict

from nltk.stem.wordnet import WordNetLemmatizer
lmtzr = WordNetLemmatizer()

from nltk.tag import StanfordNERTagger
eng_tagger = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')

"""
from nltk.parse.stanford import StanfordDependencyParser
eng_parser = StanfordDependencyParser(model_path=u'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')
"""
#import en_nb

from pattern.en import  pluralize, singularize

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


def _isplural(w):
        word = w.lower()
        singula = singularize(word)
        if singula == word:
            return False
        else:
            return True

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


def replace_nsubj(tokens, nsubj):
    """ update the subj of the sentence """

    #import pdb; pdb.set_trace()
    person_taggers = []
    org_taggers = []
    for token, title in eng_tagger.tag(tokens):
        if token.lower() in nsubj.lower().split():
            if token == 'the' or token == 'The': 
                    continue
            if title == 'PERSON':
                    person_taggers.append(token)
            elif title == 'ORGANIZATION':
                    org_taggers.append(token)
            else:
                    org_taggers.append(token)

    nsubj2 = ""
    #import pdb; pdb.set_trace()
    if len(nsubj)>0:
        if (('it' in nsubj.lower().split()) or ('they' in nsubj.lower().split())):
            nsubj2 = nsubj
        else:
            if len(person_taggers) > 0:
                nsubj2 = "He"   # 'he' will be replaced with 'he/she'
            elif len(org_taggers) > 0:
                if _isplural(org_taggers[-1]) or (org_taggers[-1].lower() == 'they'):
                    nsubj2 = "They"
                elif org_taggers[-1].lower() == 'he':
                    nsubj2 = "He"
                elif org_taggers[-1].lower() == 'she':
                    nsubj2 = "She"
                else:
                    nsubj2 = "It"
            else:
                pass
        
    return nsubj2 + " "


def include_aux(node_list, root_ind, nsubj):
    """ update the nsubj"""
    auxpass_ind = 0
    for nd in node_list:
        if root_ind == nd[0]:
            if ('auxpass' in nd[4].keys()):
                    auxpass_ind = nd[4]['auxpass'][0]
    return nsubj     


class Tree:
    def __init__(self, data):
        self.data = data
        self.kids = []
        
    def add(self, word):
        self.kids.append(word)



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

        
if __name__ == '__main__':
        main()

