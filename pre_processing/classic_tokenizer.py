# -*- coding: utf-8 -*-
'''
Created on Jan 1, 2017

@author: A.Khateeb
'''
from nltk import word_tokenize
import os
import codecs
import io
from pre_processing.stemmer import stemm

FILE_ENCODING = 'utf-8'

def tokenize(text,ar_stem=False):
    try:
        path = os.path.dirname(__file__)
        stops = io.open(path+"\stop_words.txt", 'r', encoding=FILE_ENCODING).read().split()
        words = word_tokenize(text)
        # remove stop words
        words = [stemm(w,ar_stem) for w in words if unicode(w) not in stops and len(w) > 2]
        
    except Exception as e:
        print (u"ERROR: {}").format(e) 
        exit(0) 
#     i = 0
#     for ee in stops:
#         i = i + 1
#         print (u"[{}]: {}\t".format(i,ee.decode(FILE_ENCODING)))
    return words

if __name__ == "__main__": tokenize("test this sents.")   