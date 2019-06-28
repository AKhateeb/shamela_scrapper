# -*- coding: utf-8 -*-
'''
Created on Dec 27, 2016

@author: A.Khateeb
'''

Collectors_Symbols = dict()
"""
each person (rawi) has been considered by some/one/none collector
the following dictionary has been set due to IBN-HAJAR Emam's Rules
"""
# Collectors_Symbols = {
#     "Al-Bukahry"    : [u'خ',u'خت',u'بخ',u'عخ',u'ر',u'ي'],
#     "Muslim"        : [u'م',u'مق'],
#     "Abo-Dawood"    : [u'د',u'مد',u'صد',u'خد',u'قد',u'ف',u'ل'],
#     "Al-Termithy"   : [u'ت',u'تم'],
#     "Al-Nasaey"     : [u'س',u'عس',u'سي',u'ص'],
#     "Ibnu-Majah"    : [u'ق',u'فق'],
#     "Malek"         : [u'كد',u'كن']
#     }
Collectors_Symbols = {
     "B1"    :    u'خ',
    "B2"    :    u'خت',
    "B3"    :    u'بخ',
    "B4"    :    u'عخ',
    "B5"    :    u'ر',
    "B6"    :    u'ي',
    "M1"    :    u'م',
    "M2"    :    u'مق',
    "A1"    :    u'د',
    "A2"    :    u'مد',
    "A3"    :    u'صد',
    "A4"    :    u'خد',
    "A5"    :    u'قد',
    "A6"    :    u'ف',
    "A7"    :    u'ل',
    "T1"    :    u'ت',
    "T2"    :    u'تم',
    "N1"    :    u'س',
    "N2"    :    u'عس',
    "N3"    :    u'سي',
    "N4"    :    u'ص',
    "I1"    :    u'ق',
    "I2"    :    u'فق',
    "all"   :    u'ع',
    "none"  :    u'تمييز',
    "some"  :    u'4' # all except Bukhary & Muslim
    }
def get_collector_keys(in_list):    
#     for k, v in Collectors_Symbols.items():
#         if v == value:
#             yield k
    keys = [key for key,sym in Collectors_Symbols.items() for token in in_list if sym == token and (len(token) <= 2 or token == u"تمييز") ]
    return keys
# keys = [key for key,sym in Collectors_Symbols.items() for token in Body.split()[-5:] if sym == token and (len(token) <= 2 or token == u"تمييز") ]
# # Hello :) we recommend to dispart loops if u did'nt understand what should the output looks like 27/12/2016
                            
AR_LETTER = dict()
"""
ARABIC Letters: you can have the matching word in Rnglish by the Letter it self or the letter word
"""
AR_LETTER = {
    u"الألف"     : ["ALEF"  , u'\u0627'],
    u"الباء"    : ["BAH"   , u'\u0628'],
    u"التاء"    : ["TAH"   , u'\u062a'],
    u"الثاء"    : ["THAH"  , u'\u062b'],
    u"الجيم"    : ["JEEM"  , u'\u062c'],
    u"الحاء"    : ["HAH"   , u'\u062d'],
    u"الخاء"    : ["KHAH"  , u'\u062e'],
    u"الدال"    : ["DAL"   , u'\u062f'],
    u"الذال"    : ["THAL"  , u'\u0630'],
    u"الراء"    : ["RAH"   , u'\u0631'],
    u"الزاي"    : ["ZAY"   , u'\u0632'],
    u"السين"    : ["SEEN"  , u'\u0633'],
    u"الشين"    : ["SHEEN" , u'\u0634'],
    u"الصاد"    : ["SAD"   , u'\u0635'],
    u"الضاد"    : ["DHAD"  , u'\u0636'],
    u"الطاء"    : ["TAH"   , u'\u0637'],
    u"الظاء"    : ["ZAH"   , u'\u0638'],
    u"العين"    : ["AEIN"  , u'\u0639'],
    u"الغين"    : ["GHAIN" , u'\u063a'],
    u"الفاء"    : ["FAH"   , u'\u0641'],
    u"القاف"    : ["QAF"   , u'\u0642'],
    u"الكاف"    : ["KAF"   , u'\u0643'],
    u"اللام"     : ["LAM"   , u'\u0644'],
    u"الميم"    : ["MEEM"  , u'\u0645'],
    u"النون"    : ["NOON"  , u'\u0646'],
    u"الهاء"    : ["HAH"   , u'\u0647'],
    u"الواو"    : ["WAW"   , u'\u0648'],
    u"الياء"    : ["YAH"   , u'\u064a'],
}

def get_en_letter_word(letter,ret="EN"):
    ret_val = ''
    if AR_LETTER.has_key(letter): # letter = الباء
        if ret=="EN":
            ret_val = AR_LETTER[letter][0]
        else:
            ret_val = AR_LETTER[letter][1]
    else:
        for key, val in AR_LETTER.items():
            if letter == val[1]:
                if ret == "EN":
                    ret_val = val[0]
                else:
                    ret_val = key
    return ret_val      