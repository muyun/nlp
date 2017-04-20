#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: wenlong
compatible with the AMALGrAM pkg
"""
import nltk
#import codecs

import os

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

def exec_ssh(filename):
    bashCommand = "./sst.sh " + filename
    os.system(bashCommand)


def main():
    filename = "example_"
    strs = "He eats an apple ."

    write_file(filename, strs)
    exec_ssh(filename)


if __name__ == '__main__':
    main()
