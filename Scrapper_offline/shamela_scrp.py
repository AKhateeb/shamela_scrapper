# -*- coding: utf-8 -*-
'''
Created on Dec 31, 2016
Multi-Dialect Article Classifier
@author: A.Khateeb
'''
import re, codecs
from bs4 import BeautifulSoup
from mysql.connector import Error as sq_error
import mysql.connector as sq
import os
import sys
import string
reload(sys)
sys.setdefaultencoding('Cp1252')  # @UndefinedVariable

class Shamela_scrp():

    FILE_ENCODING = 'windows-1256'
    category = ''
    Mask = u"{}\\{}\\{}.htm" # category_name \ folder_name \ filename.htm
    SOURCE_DIR = u"C:\\Users\\A.Khateeb\\workspace\\HOMEWORK\\RAW\\"

    def __init__(self,params=dict()):
        # DEFAULT VALUES
        MIN_TITLE = 10
        MAX_TITLE = 75
        MIN_BODY  = 900
        MAX_Body  = 3000
        MIN_APPAEND = 75
        MAX_APPENDED = 700
        CATEGORY = 'NI'
        PURIFICATION = ['tag','number','symbol','space']

        self.category = params.get("category",CATEGORY)
        self.min_title = params.get("min_title",MIN_TITLE)
        self.max_title = params.get("max_title",MAX_TITLE)
        self.min_body = params.get("min_body",MIN_BODY)
        self.max_body = params.get("max_body",MAX_Body)
        self.min_append = params.get("min_append",MIN_APPAEND)
        self.max_append = params.get("max_append",MAX_APPENDED)

        self.purification = params.get("purification",PURIFICATION)
        config = {"host":'localhost',"user":'python',"password":'0000',"db":'mdac'}
        self.db_connect(config)

    def db_connect(self,config=dict()):
        """
        Connect to MYSQL Database :) 31/12/2016
        """
        try:
            self.conn = sq.connect(
                host=config["host"],
                user=config["user"],
                passwd=config["password"],
                db=config["db"],
                charset='utf8',
                use_unicode=True)

            if self.conn.is_connected():
#                 print ("Connected to MySQL database")
                self.cursor = self.conn.cursor()
        except sq_error as e:
            print ("DB_ERROR: {}".format(str(e)))
            return

    def purify(self,element):
        """
        we need to clean text, can't use p.text
        because it's converted to unicode
        first: clear HTML Tags
        second: remove numbers and undesirable symbols
        third: replace multiple spaces and tabs with one space
        """
        if "tag" in self.purification:
            element = re.sub(u"([<]{1}/?[a-z=#\"\'0-9 ]+[>]{1})+", "", element)
        if "number" in self.purification:
            element = re.sub(u"[0-9\-\+*/]+", "", element)
        if "symbol" in self.purification:
            element = re.sub(u"[\]\[\)\(\^%$#@!~*\\\?\\}\{<>_\.]+", "", element)
        if "space" in self.purification:
            element = re.sub(u"[ \t\n]+|([<]br/?[>]){2,}", " ", element)
        return element

    def scrap(self):
        path = self.SOURCE_DIR+self.category
        for Fi in os.listdir(path):
#             print (u"\n{} >> Chuncking File [{}]....\n".format(self.category,Fi))
            try:
                with codecs.open(self.Mask.format(path,Fi,Fi), 'rb', self.FILE_ENCODING) as f:
                    html = f.read()
                    soup = BeautifulSoup(html,'lxml') # we recommend to use lxml, Html.parser gives bad output
                    elms = [x for x in soup.find_all('ul')][-1].find_all('p') # ul[0] = introduction, ul[1] = elements
                    yield [Fi,elms] # we only have one <ul> in a file
            except IOError as e:
                print (u"PATH of file is NOT valid, ERROR: {}").format(e)
                exit(0)

    def parse(self,file_name,elements=[]):
        B = []
        inserted = 0
        title = ''
        Body = ''
        for p in elements:
            for element in re.compile(u"[<]br/?[>]",).split(unicode(p)):
                element = self.purify(element)
                if len(element) in range(self.min_title,self.max_title) and not re.match(u"[-_\.*\+]{2,}", element):
                    title = element
#                     print (u"Title: {}".format(title))
                else:
                    B.append(element)
                if len(B) > 0 and len(string.join(B,' ')) >= self.min_body:
                    #yield [file_name,title,Body]
                    Body = string.join(B,u' ؛ ')
#                     print (u"Body: {}".format(Body))
                    args = [file_name,title,Body,self.category,'book']
                    self.store(args)
                    inserted = inserted +1
                    B = []
                else: continue
        return inserted

    def store(self,args):
        try:
            self.cursor.callproc('insert_article',args)
            self.conn.commit() # so important .. no change applied without it
        except sq_error as e:
            print ("DB_ERROR: {}".format(e))
            exit(1)

def main():
    total = 0
    print(u"Start Scrapping :)")
    print(u"---+---")*5
    param = {"category": "Economy","purification":["space","tag","symbol"]}
    cats = ['economy']
    for categ in cats:
        param["category"] = categ
        obj = Shamela_scrp(param)
        for [fi,scp] in obj.scrap():
            result = obj.parse(fi,scp)
            total += result
            print (u"{} >> File: {}, Records: ({})").format(obj.category,fi,result)
#     economy = shamela_scrp(param)
#     for [fi,scp] in economy.scrap():
#         result = economy.parse(fi,scp)
#         total += result
#         print (u"{} >> File: {}, Records: ({})").format(economy.category,fi,result)
    print (u"\nTOTAL of {}: <{}>").format(obj.category,total)
if __name__ == "__main__": main()
