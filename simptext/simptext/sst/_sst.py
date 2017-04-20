#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: wenlong
compatible with the AMALGrAM pkg
"""
import nltk
#import codecs

import os
import subprocess

#_path = "/Users/zhaowenlong/workspace/proj/dev.nlp/simptext/simptext/sst/"
_path = "./sst/"

def get_word_pos_(w):
    #
    pos = nltk.tag.pos_tag([w])[0][1]
    return w+"\t"+pos


def write_file(filename, strs):
    text = nltk.word_tokenize(strs)
    word_pos_tag = nltk.pos_tag(text)

    elem=""
    for item in word_pos_tag:
        elem = elem + item[0]+"\t"+item[1]+"\n"

    #import pdb; pdb.set_trace()
    f = open(filename, 'w')
    f.write(elem)
    f.close()

def _exec_ssh(filename):
    ret = ""
    bashCommand1 = _path + "sst.sh " + filename

    #import pdb; pdb.set_trace()
    os.system(bashCommand1)

    bashCommand2 = "cut -f2 " +  filename+".pred.sst"
    import pdb; pdb.set_trace()
    _ret = print(subprocess.Popen(bashCommand2, shell=True,stdout=subprocess.PIPE).stdout.read())

    ret = subprocess.Popen(bashCommand2, shell=True,stdout=subprocess.PIPE).stdout.read()

    import pdb; pdb.set_trace()

    return ret

def exec_ssh(filename, strs):
    ret = ""
    #_strs = _path+strs
    _filename = _path+filename
    write_file(_filename, strs)

    #import pdb; pdb.set_trace()
    ret = _exec_ssh(_filename)

    import pdb; pdb.set_trace()
    return ret

def main():
    filename = "example_"
    strs = "He eats an apple ."

    ret = exec_ssh(filename, strs)
    return ret


if __name__ == '__main__':
    main()
