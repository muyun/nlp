"""
 This is from Ms. XIE

"""
import kenlm
import os
import argparse
import sys, operator, time, nltk
import gensim
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import StanfordTokenizer
from nltk.tag import StanfordPOSTagger
st = StanfordPOSTagger('english-bidirectional-distsim.tagger')

from nltk.tag import StanfordNERTagger
eng_tagger = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')

from nltk.parse.stanford import StanfordDependencyParser
eng_parser = StanfordDependencyParser(model_path=u'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')

ken_model = kenlm.Model('/Users/zhaowenlong/workspace/proj/dev.nlp/simptext/simptext/models/bin/europarl.bin')
w2v_model=gensim.models.Word2Vec.load_word2vec_format('/Users/zhaowenlong/workspace/proj/dev.nlp/simptext/simptext/models/bin/en.bin',binary=True)
lmtzr = WordNetLemmatizer()
EDB_list=[]

def isplural(w):
        word = w.lower()
        lemma = lmtzr.lemmatize(word, 'n')
        plural = True if word is not lemma else False
        return plural

def get_triples(node):
    """
    Extract dependency triples of the form:
    (32, u'week', u'NN', u'nmod', defaultdict(<type 'list'>, {u'case': [30], u'det': [31]}))
    """

    #import pdb; pdb.set_trace()
    return (node[1]['address'], node[1]['word'], node[1]['ctag'], node[1]['rel'], node[1]['deps'])      
        

def _Stem(sub_sent,edblist):
	#words = nltk.word_tokenize(sub_sent)
	words = StanfordTokenizer().tokenize(str(sub_sent))
	tokens = st.tag(words)
	#print "tokens: ", tokens
        #print "sub_sent: ", sub_sent
	#tokens = "nltk.pos_tag(words)

 	"""
        result = list(eng_parser.raw_parse(sub_sent))[0]
        node_list = [] # dict (4 -> 4, u'said', u'VBD', u'root', [[18], [22], [16], [3]])
        for node in result.nodes.items():
                node_list.append(get_triples(node))

        root = ""
        root_ind = node_list[0][4]['root'][0]
        for nd in node_list:
                if root_ind == nd[0]:
                        root=nd[1]

        nsubj_ind = 1
        for nd in node_list[1:]:
                if (root in nd) and ('nsubj' in nd[4].keys()):
                        nsubj_ind = nd[4]['nsubj'][0]
                        
        org_taggers = words[nsubj_ind-1]
        """
        nsubj_ind = 1
        if len(words) > 0:
                nsubj_taggers = words[nsubj_ind-1]
        else:
                nsubj_taggers = ""
        
	word_list = []
	word_pre = []
	pos = ['NNP','NNPS','POS',',','.','\'','$','WRB','MD','SYM','TO','WP','WDT',':','CD','DT','EX', 'PRP','PRP$']
	v_pos = ['VBD','VBG','VBN','VBP','VBZ']	
	n_pos = ['NNS']
        n_tag =['NN', 'NNS', 'NNP', 'NNPS']

        #import pdb; pdb.set_trace()
        _taggers = []
	for e in tokens:
		if e[1] not in pos:
			temp = e[0].lower()
			if e[1] in v_pos:
				word_list.append(lmtzr.lemmatize(temp,'v'))
				word_pre.append(lmtzr.lemmatize(temp,'v'))
			elif (e[1] in n_pos) and (e[0] != nsubj_taggers):
				word_list.append(lmtzr.lemmatize(temp))
				word_pre.append(lmtzr.lemmatize(temp))
			else:
				word_list.append(temp)
				word_pre.append(temp)
		else:
			word_pre.append(e[0])

                if e[1] in n_tag:
                        _taggers.append(e[0])
                        
	sub_words = []
	#Print word_pre

        #import pdb; pdb.set_trace()
	for w in word_list:
		w = w.strip()
		if w and w not in edblist:
			sub_words.append(w.strip())

        # get the person name based on StanfordNERTagger
        
        #import pdb; pdb.set_trace()
        taggers = []
        if nsubj_taggers in _taggers:
                taggers.append(nsubj_taggers)
                
        """
        person_taggers = []
        org_taggers = []
        for token, title in eng_tagger.tag(words):
                if token in taggers:
                        if title == 'PERSON':
                                person_taggers.append(token)
                        elif title == 'ORGANIZATION':
                                org_taggers.append(token)
                        else:
                                org_taggers.append(token)
        """                                     
	#import pdb; pdb.set_trace()
	return sub_words, word_pre, taggers

def Initial(fin): #load EDB_List
	flist = open(fin,'r')
	ltines = flist.readlines()
	for l in ltines:
		if l:
			EDB_list.append(l.strip())
		else:
			break
	return True

def Generate_candidates_topN(target_word,sent,N,edblist):
	if target_word not in w2v_model.vocab: return [target_word]
	result = w2v_model.most_similar(target_word,topn=2000)
	tsum = 0
	temp = []
	for e in result:
		if tsum == N: break
		if e[0] in edblist:
			temp.append(e[0])
			tsum = tsum + 1
		else: continue
	return temp

def kenlm_topn(subs_sent,n,t_sent):
	dic = {}
	for line in subs_sent:
		if line:
			word = line.split('@')[0]
			sent = line.split('@')[1]
			dic[word] = ken_model.score(sent,bos = True, eos = True)
			#print word,dic[word]
		else:
			break
	dict_top10 = sorted(dic.iteritems(),key=lambda d:d[1],reverse=True)
	len_dit = len(dict_top10)
	subs=[]
	for i in range(len_dit):
		w,p=dict_top10[i]
		subs.append(w.strip())
		if i == n: break
	return subs


def _process_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i1', default=r"/home/wenxixie/www/EDB_List.txt", help='input directory (automatic find and read each file as a document)')
    parser.add_argument('-i2', default=r"Mr. Hall 's old factory is still on Oklahoma Avenue , but the metal fabrication plant where Mr. Larson worked finally closed last year after withering for decades .", help='input sentence')
    parser.add_argument('-i3', default=r"finally", help='input target_word')
    return parser.parse_args(sys.argv[1:])

def _interface(sentence,edblist):
	target_words, word_pre, taggers =  _Stem(sentence,edblist)
	token_list =[]
 
        #import pdb; pdb.set_trace()
	for word in word_pre:
	        tokens = {}
                if word == "He": # is a person, subject?
                	tokens[word] = [word, "He", "She"]
                elif word == "They":
                	tokens[word] = [word, "They"]
                elif word == "It":
                	tokens[word] = [word, "It"]
                else:
                        if word not in target_words:
                                token_list.append(word)
                        else:
                                r_sent = []
			        candidates = Generate_candidates_topN(word,sentence,19,edblist)
			        for i in range(len(candidates)):
				        r_sent.append(candidates[i] + "@" + sentence.replace(word,candidates[i]))
			        sub_top10 = kenlm_topn(r_sent,9,sentence)
			        if word not in sub_top10:
			        	sub_top10.insert(0,word)
			        tokens[word] = sub_top10
                                
                if tokens: token_list.append(tokens)
                
	return token_list
	

if __name__ == '__main__' :
	args = _process_args()
	word_list = _interface(args.i2)
	print word_list

	
