# -*- coding: utf-8 -*-
"""
   print the split rate

"""
import sys, re, codecs, csv
from collections import OrderedDict

import nltk.corpus
import nltk.tokenize.punkt
import nltk.stem.snowball
from nltk.corpus import wordnet

import dt_sent
#import wordcal

import string

# the English stopwords and extend with punctuation
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(string.punctuation)
stopwords.append('')

# create tokenizer and stemmer
from nltk.tokenize import StanfordTokenizer
#tokenizer = nltk.tokenize.punkt.PunktWordTokenizer()
lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()

reload(sys)
sys.setdefaultencoding('utf-8')

def get_wordnet_pos(pos_tag):
    if pos_tag[1].startswith('J'):
        return (pos_tag[0], wordnet.ADJ)
    elif pos_tag[1].startswith('V'):
        return (pos_tag[0], wordnet.VERB)
    elif pos_tag[1].startswith('N'):
        return (pos_tag[0], wordnet.NOUN)
    elif pos_tag[1].startswith('R'):
        return (pos_tag[0], wordnet.ADV)
    else:
        return (pos_tag[0], wordnet.NOUN)


def print_mturk_sent(filename, sent_file):
    num_sentences = 0
    num_splitted_sentences = 0
    #data = json.load(open(datafile))
    docs = OrderedDict() # store the info - docs[sentence] = [id,...]

    #soup = BeautifulSoup(open(filename), "lxml")

    # number of sentences, based on the 'sent' tag
    #sentences = soup.find_all("instance")
    #num_sentences = len(sentences)

    #p = re.compile(r'<.*?>')
    #import pdb; pdb.set_trace()
    output = OrderedDict()
    f = open(filename, 'rU')
    num = 0
    res = ""
    for line in f:
        line = line.strip('\n')
        if line:
            #import pdb; pdb.set_trace()
            num_sentences = num_sentences + 1
            #print(sentence)
            #sent = str(p.sub('', str(sentence)))
            #se = re.sub(r'^”|”$', '', sent)
            #se = sentence.context.get_text()
            #sent = str(BeautifulSoup(sentence).text)
            obj = line.split("\t")
            se = re.sub(r'^"|"$', '', obj[0])
            print(se)
            # write the sentence
            #res = ""
            #res = punct.simp_syn_sent_(se)
            #res = coordi.simp_syn_sent_(se)
            #res = subordi.simp_syn_sent_(str(se))
            #res = adverb.simp_syn_sent_(str(se))
            #res = parti.simp_syn_sent_(str(se))
            #res = adjec.simp_syn_sent_(str(se))
            #res = appos.simp_syn_sent_(str(se))
            #res = passive.simp_syn_sent_(str(se))
            #res = paratax.simp_syn_sent_(str(se))
            #res = alg.simp_passive_sent(str(re))
            _res = dt_sent.simp_syn_sent(str(se))
            if len(_res)>0:
                (s1, s1_child, s2, s2_child, res) = dt_sent._get_split_ret(_res)
                print "res: ", res
            else:
                res = _res

            if _res: # the
                num_splitted_sentences = num_splitted_sentences + 1

            #import pdb; pdb.set_trace()
            output[se] = res
            #import pdb; pdb.set_trace()

            with open(sent_file, 'a') as outfile:
                outfile.write(str(se)+'\n')
                outfile.write("OUTPUT: " + res + '\n')
                #outfile.write('-----------------------\n')
                #json.dump(output, outfile, indent=2)

            """
            num = num + 1
            if num == 200:
                break
            """

    return num_sentences, num_splitted_sentences


def check_sent_similar(sent1, sent2, threshold=0.5):
    """ check whether the two sents are the similar """
    pos_1 = map(get_wordnet_pos, nltk.pos_tag(StanfordTokenizer().tokenize(sent1)))
    pos_2 = map(get_wordnet_pos, nltk.pos_tag(StanfordTokenizer().tokenize(sent2)))
    lemmae_1 = [lemmatizer.lemmatize(token.lower().strip(string.punctuation), pos) for token, pos in pos_1 \
                    if token.lower().strip(string.punctuation) not in stopwords]
    lemmae_2 = [lemmatizer.lemmatize(token.lower().strip(string.punctuation), pos) for token, pos in pos_2 \
                    if token.lower().strip(string.punctuation) not in stopwords]

    return (lemmae_1 == lemmae_2)

def is_similar(sent1, sent2):
    """ if the sent is multi-sentence;
        Assume the sentences are 2-splitted
    """
    #import pdb; pdb.set_trace()
    str1 = sent1.split('.')
    str2 = sent2.split('.')

     # Assume sent1 and sent2 are two splitted sentences
    _str1 = str1[0] + ' . '
    _str2 = str2[0] + ' . '
    if check_sent_similar(_str1, _str2):
           # check 2nd part
        _str1 = str1[1] + ' . '
        _str2 = str2[1] + ' . '
        if check_sent_similar(_str1, _str2):
            return True
        else:
            return False
    else:
        return False


def cal_mturk_sent(filename, gt):
    f = open(filename, 'rU')
    _num_output = 0
    num_negative = 0
    num_false_positive = 0
    num_true_negative = 0
    num_false_negative = 0
    num_true_positive = 0
    _num_false_positive = 0
    _num_true_negative = 0
    _num_false_negative = 0
    _num_true_positive = 0
    num_positive = 0
    num = 0
    len_input = 0
    len_output = 0
    _input = ""
    _sp = ""
    _gen = ""
    output = OrderedDict()
    for line in f:
        line = line.strip('\n')

        #import pdb; pdb.set_trace()
        if "OUTPUT" not in line :
            match = re.search(r'--+', line)
            if match:
                pass
            else:
                _input = line
                len_input = len(re.findall("\w+", line))
            #print "Input: ", line

        #import pdb; pdb.set_trace()
        else:
            #print "gt-out: ", gt[num]
            #print "out: ", line
            #len_output = len(re.findall("\w+", line))
            #import pdb; pdb.set_trace()
            #num_output = num_output + 1
            #print(sentence)
            #sent = str(p.sub('', str(sentence)))
            #se = re.sub(r'^”|”$', '', sent)
            #se = sentence.context.get_text()
            #sent = str(BeautifulSoup(sentence).text)
            ot_flag = line.split(':')[0]
            ot = line.split(':')[1].strip() # having output or not

            #import pdb; pdb.set_trace()
            if ot_flag == "OUTPUT":  # the num
                _num_output = _num_output + 1

            # have the output (complex sentence), consider is as positive
            # increase the standard -> is it similar with the Glod one?
            if ot and is_similar(ot, gt[num]):
                num_positive = num_positive + 1
                _sp = ['Y'] # based on similar standard
                #_gen = ['Y']

                if gt[num] != 'x':  # complex sentences
                    num_true_positive = num_true_positive + 1
                else:
                    num_false_positive = num_false_positive + 1

            else: # don't have the output, and not similar
                num_negative = num_negative + 1
                _sp = ['N']

                if gt[num] != 'x':
                    num_false_negative = num_false_negative + 1
                else:
                    num_true_negative = num_true_negative + 1


            output[num] = [_input,
                         gt[num],
                         ot,
                         _sp,
                        _gen]

            #import pdb; pdb.set_trace()
            with codecs.open('mturk_sent_l5.csv', 'a', encoding='utf-8') as outfile:
                wr = csv.writer(outfile, delimiter = ',', quoting = csv.QUOTE_ALL)
                wr.writerow(output[num])

            num = num + 1
            if num == 294:
                break

    #import pdb; pdb.set_trace()
            #match = re.search(r'(^(#OUTPUT):(\w*))', line)
    print "#num_negative: ", num_negative
    print "#num_false_positive: ", num_false_positive
    print "#num_true_positive: ", num_true_positive
    print "#num_false_negative: ", num_false_negative
    print "#num_true_negative: ", num_true_negative
    print "#num_positive: ", num_positive
    print "#_num_output: ", _num_output

    return num_negative, num_positive


def main():
    dir="/Users/zhaowenlong/workspace/proj/dev.nlp/simptext/simptext/"
    # print the inter data in the syntactic simplification
    #filename = dir + "utils/semeval/test/lexsub_test.xml"
    filename = dir + "utils/mturk/lex.mturk.txt"
    sent_file = dir + "tests/sent_mturk_l5_.md"
    gt_file = dir + "dataset/simplify_testset_0814.xlsx"

    #_info = print_mturk_sent(filename, sent_file)
    #print "Type: Paratax Clauses:"
    #print "#sentence in mturk: ", _info[0]
    #print "#sentence with Syntactic simplification: ", _info[1]


    #sent1 = "it was often convenient regard man as clockwork automata."
    #sent2 = " it was often convenient regard man as clockwork automata."
    #print(check_sent_similar(sent1, sent2))
    #print(is_similar(sent1, sent2))

    # recall and precision
    #filename = dir + "utils/testset_groundtruth.md"
    #filename = dir + "utils/coordi_mturk_l1_.json"
    #filename = dir + "utils/testset_gt_adverb.md"
    #filename = dir + "utils/testset_gt_appos.md"

    #filename = dir + "utils/testset/sent_mturk_l4_.md"
    gt = dt_sent.read_xlsx_file(gt_file, 1, 2)
    _info = cal_mturk_sent(sent_file, gt)


if __name__ == '__main__':
    main()
