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

class Watan_scrp():
    
    FILE_ENCODING = 'windows-1256'
    category = ''
    Mask = u"{}\\{}" # category_name \ folder_name \ filename.htm
    SOURCE_DIR = u"C:\\Users\\A.Khateeb\\workspace\\HOMEWORK\\RAW\\EXTRA\\WATAN\\"
    
    def __init__(self,category='NI'):
        # DEFAULT VALUES    
        if category != 'NI':
            self.category = category
        
        self.purification = ['symbol','space']
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
        path = self.SOURCE_DIR+self.category+u"\\"+self.category+".html\\"
        for Fi in os.listdir(path)[:1000]:
#             print (u"\n{} >> Chuncking File [{}]....\n".format(self.category,Fi))
            try:
                with codecs.open(self.Mask.format(path,Fi), 'rb', self.FILE_ENCODING) as f:
                    html = f.read()
                    soup = BeautifulSoup(html,'lxml') # we recommend to use lxml, Html.parser gives bad output
                    yield [Fi,soup.find('body').text]
            except IOError as e:
                print (u"PATH of file is NOT valid, ERROR: {}").format(e) 
                exit(0)
   
    def parse(self,file_name,text):
        inserted = 0
        title = u"watan_{}".format(self.category)
        Body = self.purify(text)
        args = [file_name,title,Body,self.category,'magazine']
        self.store(args)
        inserted = inserted +1 
        return inserted
    
    def store(self,args):
        try:
            self.cursor.callproc('insert_article',args)  
            self.conn.commit() # so important .. no change applied without it
            print (args[2][:50])
        except sq_error as e:
            print ("DB_ERROR: {}".format(e))
            exit(1)  
                                        
def main():     
    total = 0
    print(u"Start Scrapping :)")
    print(u"---+---")*5
    
    cats = ['economy','politics','religion','sport','art'] 
    for categ in cats:
        obj = Watan_scrp(categ)
        for [fi,scp] in obj.scrap(): 
            total += obj.parse(fi,scp)  
        print (u"{} >> File: {}, Records: ({})").format(obj.category,fi,total)
#     economy = shamela_scrp(param)   
#     for [fi,scp] in economy.scrap():
#         result = economy.parse(fi,scp)  
#         total += result   
#         print (u"{} >> File: {}, Records: ({})").format(economy.category,fi,result)
    print (u"\nTOTAL of {}: <{}>").format(obj.category,total)
if __name__ == "__main__": main()            
            
            