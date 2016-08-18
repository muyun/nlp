import kenlm
import os
import argparse
import sys, operator, time, nltk
import gensim
from nltk.stem.wordnet import WordNetLemmatizer

ken_model = kenlm.Model('/Users/zhaowenlong/workspace/proj/dev.nlp/simptext/utils/model/bin/europarl.bin')
w2v_model=gensim.models.Word2Vec.load_word2vec_format('/Users/zhaowenlong/workspace/proj/dev.nlp/simptext/utils/model/bin/en.bin',binary=True)
lmtzr = WordNetLemmatizer()
EDB_list=[]

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
		if tsum == N : break
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

def _interface(word,sentence,edblist):
	r_sent = []
	candidates = Generate_candidates_topN(word,sentence,19,edblist)
	for i in range(len(candidates)):
		r_sent.append(candidates[i] + "@" + sentence.replace(word,candidates[i]))
	sub_top10 = kenlm_topn(r_sent,9,sentence)
	return sub_top10
	

if __name__ == '__main__' :
	args = _process_args()
	Initial(args.i1)
	ws = ['finally','factory']
	word_list = _interface(ws,args.i2)
	print word_list

	
