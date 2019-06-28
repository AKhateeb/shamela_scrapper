# -*- coding: utf-8 -*-
'''
Created on Jan 1, 2017

@author: A.Khateeb
'''
import re
from stemmer import ArabicLightStemmer
# from purifier import purify


def stemm(word,ar_stem = False):
    # Delete non-Arabic charachters
    word = re.sub(u"[^أ-ي]+"," ",word) # [^\p{L}\p{Nd}]+
    # Delete vacals (if NOT selected in Purify)
    word = re.sub(u'[\u064b\u064c\u064d\u064e\u064f\u0650\u0652\u0651]',"",word)
    # Delete TATWEEL
    word = re.sub(u"[ـ]+","",word)
    ar = ArabicLightStemmer()
    if ar_stem:
        ar.lightStem(word)
        word = ar.get_stem()
    
    return word
def main():
    te = u"بسم! الله الرَّحمن÷ الر    _حــي، م4الك يوAم الدين/ٌُ إيياك*"
    te = u"لا تكونين للعيش مجروحة الفؤاد إنما الرزق على رب العباد"
    stemm(te)
#     print (purify(te))
    
    
if __name__ == "__main__": main()   