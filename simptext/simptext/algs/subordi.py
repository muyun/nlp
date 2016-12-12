# -*- coding: utf-8 -*-
"""
   utils.base
   ~~~~~~~~~~
   base common function
"""
#from itertools import chain
from collections import defaultdict

from nltk.tokenize import StanfordTokenizer
#from nltk.tokenize import wordpunct_tokenize


from nltk.parse.stanford import StanfordDependencyParser
eng_parser = StanfordDependencyParser(model_path=u'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')

from nltk.tag import StanfordNERTagger
eng_tagger = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')

#from algs import base
import base

PUNCTUATION = (';', ':', ',', '.', '!', '?')

def simp_subordi_sent(tokens, node_list):
    # C1 and C2  must have the own subject
    #PUNCT = ','
    # the subordinating conjunction
    dict1 = {   'after': 'Then',
                'although': 'But',
                'though': 'But',
                'since': 'Therefore',
                'because': 'Therefore',
                'as': 'Therefore',
                'even though': 'Even so',
                'while': 'But',
                'if': 'Suppose',
                'when': 'At the time'
            }

    dict2 = {
                'since': 'This is because',
                'because': 'This is because',
                'as': 'This is because',
                'so': 'So',
                'before': 'Then',
                'while': 'But',
                'where': 'There'
    }

    root = ""
    root_ind = node_list[0][4]['root'][0]
    for nd in node_list:
        if root_ind == nd[0]:
            root=nd[1]

    strs = ""
    #split_ind = 0
    mark_ind = 0
    for nd in node_list[1:]:
        #import pdb; pdb.set_trace()
        #print(nd)
        if (root in nd) and ('advcl' in nd[4].keys()):
            # C1 and C2 have its own subject
            
            #print "conj: ", nd
            #print "conj node: ", nd[4]['conj']
            pass

        if (root in nd) and ('advcl' in nd[4].keys()):
            advcl_ind = nd[4]['advcl'][0]

            #import pdb; pdb.set_trace()
            mark_list = []

            nsubj = ""
            nsubj_ind = 0
            full_nsubj_ind = 0
            det_ind = 0
            nsubj_word = ""
            if ('nsubj' in nd[4].keys()):
                nsubj_ind = nd[4]['nsubj'][0]
                nsubj_dict = {}
                nsubj_compound_list = []
                amod_list = []
                det_ind = 0
                #import pdb; pdb.set_trace()
                for _nd in node_list:
                    #import pdb; pdb.set_trace()
                    if (nsubj_ind == _nd[0]):
                        #import pdb; pdb.set_trace()
                        nsubj_dict = _nd[4]
                        if ('amod' in nsubj_dict.keys()):
                            amod_list = nsubj_dict['amod']
                        if ('compound' in nsubj_dict.keys()):
                            nsubj_compound_list = nsubj_dict['compound']
                        if ('det' in nsubj_dict.keys()):
                            det_ind = nsubj_dict['det'][0]

                #import pdb; pdb.set_trace()
                for j in amod_list:
                    nsubj = nsubj + " " + tokens[j]
                for i in nsubj_compound_list:
                    nsubj = nsubj + " " + tokens[i]
                if det_ind > 0:
                    nsubj = tokens[det_ind] + " " + nsubj + " " + tokens[nsubj_ind]
                else:
                    nsubj = nsubj + " " + tokens[nsubj_ind]

                #import pdb; pdb.set_trace()
                full_nsubj_ind = tokens.index(nsubj.split()[0])
                nsubj = nsubj.strip()
                nsubj = nsubj[0].upper() + nsubj[1:] + " "

            advcl_dict = {}
            for _nd in node_list[1:]: #BUG
                if advcl_ind == _nd[0]:
                     advcl_dict = _nd[4]
                     mark_list = _nd
                     break                
            # the nsubj of the advcl
            #import pdb; pdb.set_trace()
            nsubj_advcl_word = ""
            advcl_det_ind =0
            if ('nsubj' in advcl_dict.keys()):
                nsubj_advcl_ind = advcl_dict['nsubj'][0]
                for nnd in node_list[1:]:
                    if nsubj_advcl_ind == nnd[0]:
                        if ('det' in nnd[4].keys()):
                            advcl_det_ind = nnd[4]['det'][0]
                        #nsubj_advcl_word = nnd[1] # get the subj of the advcl
                        #break
            if advcl_det_ind > 0:
                nsubj_advcl_word = tokens[advcl_det_ind] + " " + tokens[nsubj_advcl_ind]
            else:
                nsubj_advcl_word =  tokens[nsubj_advcl_ind]

            """
            for the sentence "Since he was hungry, he ate a banana.""
            import pdb; pdb.set_trace()
            if nsubj_word == nsubj_advcl_word:
                return strs
            """
            #import pdb; pdb.set_trace()
            if ('mark' in advcl_dict.keys()):
                #import pdb; pdb.set_trace()
                mark_ind = mark_list[4]['mark'][0]
                marker = tokens[mark_ind].lower()

                # get the marker,  delete the conjunction
                #tokens[mark_ind] = ''
                #tokens[mark_ind+1] = upper_first_char(tokens[mark_ind+1])
                # if the marker is in the dict1
                # [NOTICE]: we use the punctuation to check the sentence

                #import pdb; pdb.set_trace()
                if (marker in dict1.keys()): # if dict1, subordinated clause goes first
                    # delete the conjunction,
                    _w = dict1[marker]
                    tokens[mark_ind] = ''
                    tokens[mark_ind+1] = base.upper_first_char(tokens[mark_ind+1])

                    #[NOTICE]: we consider 1st ',' to split the sentence, and get the 2nd sentence

                    #import pdb; pdb.set_trace()
                    if nsubj_ind != 0:
                        #_str1 = tokens[:(nsubj_ind)]
                        if tokens[full_nsubj_ind].lower() == tokens[nsubj_ind].lower():
                            
                            _str1 = tokens[:nsubj_ind]
                        else:
                            if det_ind > 0:
                                _str1 = tokens[:det_ind]
                            else:
                                _str1 = tokens[:full_nsubj_ind]
                        if _str1[-1] in PUNCTUATION:
                            _str1[-1] = ''
                        str1 = ' '.join(_str1)
                        str1 = str1[0].upper() + str1[1:]
                    #print "1st sent: ", str1

                        #_str2 = tokens[nsubj_ind:]
                        if tokens[full_nsubj_ind].lower() == tokens[nsubj_ind].lower():
                            _str2 = tokens[nsubj_ind:]
                        else:
                            if det_ind > 0:
                                _str2 = tokens[det_ind:]
                            else:
                                _str2 = tokens[full_nsubj_ind:]
                    #w = _w + ' '
                        str2 = _w + ' ' + ' '.join(_str2)
                    #print "2nd sent: ", str2

                        strs = str1 + ' . ' + str2

                    else:
                        pass

                    return strs


                # if dict2, the subordinated clause goes second
                if (marker in dict2.keys()):

                    #import pdb; pdb.set_trace()
                    _w = dict2[marker]
                    tokens[mark_ind] = ''
                    #tokens[mark_ind+1] = base.upper_first_char(tokens[mark_ind+1])

                    #TODO add it before the nsubj
                    if nsubj_ind != 0:
                        if tokens[full_nsubj_ind].lower() == tokens[nsubj_ind].lower():
                            _str1 = tokens[:nsubj_ind]
                        else:
                            if det_ind > 0:
                                _str1 = tokens[:det_ind]
                            else:
                                _str1 = tokens[:full_nsubj_ind]
                        #_str1 = tokens[:(nsubj_ind)]
                        if _str1[-1] in PUNCTUATION:
                            _str1[-1] = ''

                        #str1 = ' '.join(_str1)
                        #print "1st sent: ", str1

                        #_str2 = tokens[nsubj_ind:]
                        if tokens[full_nsubj_ind].lower() == tokens[nsubj_ind].lower():
                            _str2 = tokens[nsubj_ind:]
                        else:
                            if det_ind > 0:
                                _str2 = tokens[det_ind:]
                            else:
                                _str2 = tokens[full_nsubj_ind:]
                        if _str2[-1] in PUNCTUATION:
                            _str2[-1] = ''

                        if (marker == 'before'):
                            (_str1, _str2) = (_str2, _str1)

                        str1 = ' '.join(_str1)
                        str1 = str1[0].upper() + str1[1:]
                        print "1st sent: ", str1
                    #w = _w + ' '
                        str2 = _w + ' ' + ' '.join(_str2)
                        print "2nd sent: ", str2

                        strs = str1 + ' . ' + str2 + ' . '
                    else:
                        pass

                    return strs


        #if mark_ind == 0:  # if no mark word
        # adverbial clauses [NOTICE]: consider ',' to split the sentence

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
    strs = simp_subordi_sent(tokens, node_list)
    #strs = simp_advcl_sent(tokens, node_list)
    #strs = simp_parti_sent(tokens, node_list)
    #strs = simp_adjec_sent(tokens, node_list)
    #strs = simp_appos_sent(tokens, node_list)
    #strs = simp_passive_sent(tokens, node_list)

    return strs

def main():
    #  clauses
    sent = "Since alice emith came, I left"
    sent = "Since he was late, I left."
    sent = "Since he was hungry, he ate a banana."
    sent = " Since she was thirsty , she drank water."
    #sent = " Since she was thirsty , he offered a drink. "
    #sent = "Since she was thirsty , he offered a drink."
    #sent = " Since she was hungry, they gave food. "
    sent = "Before he came, I left"
    sent = "Before he came to school, she ate an apple."
    #sent = "He weakened to a tropical storm while also dumping heavy rain on already-devastated Haiti  ."
    #sent = "John McCain polled 62.5 % in the 2008 Presidential Election while 70.9 % of Utahns opted for George W. Bush in 2004 ."
    #sent = "I feel angry when provoked"
    #sent = "After eating dinner, he goes home."
    #sent = "Peter - nobody guessed it - showed up."
    sent = "Because he liked sushi, Mr. Smith went to the restaurant."
    #sent = "Because the economy is bad, the Federal Reserve lowers the interest rate."
    #sent = "Because she was pretty, Sam liked her."
    #sent = "Although she ate something, she did not drink anything."
    #sent = "Because the economy is bad, the Federal Reserve lowers the interest rate."
    #print(simp_coordi_sent(sent))
    print(simp_syn_sent_(sent))    

        
if __name__ == '__main__':
    main()

        
