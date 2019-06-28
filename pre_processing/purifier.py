# -*- coding: utf-8 -*-
'''
Created on Jan 1, 2017

@author: A.Khateeb
'''
import re
Patterns = dict()
Patterns = {
    "number"        :  u"([0-9-\\+\*/]+[.,]*)+"  ,
    "symbol"        :  u"[\]\[\)\(\^%$÷×`#@!~*\\\?\\}\{<>_\.]+"  ,
    "non-arabic"    :  u"[^أ-ي]"  ,
    "punctuation"   :  u"[\.\,\;\،\؛\'\"\‘\:]+" ,
    "tag"           :  u"([<]{1}/?[a-z=#\"\'0-9 ]+[>]{1})+",
    "space"         :  u"[ \t\n]{2,}",
    "vocal"         :  u'[\u064b\u064c\u064d\u064e\u064f\u0650\u0652\u0651]'
    }
def purify(text, opts=["number","symbol","punctuation","space","vocal"]):
    for opt in opts:
        # it should  be replaced with a space
        if opt in ["space","punctuation"]:
            replace_by = " "
        else:
            replace_by = ""
        text = re.sub(Patterns[opt],replace_by,text)
    return text


if __name__ == "__main__": purify()   