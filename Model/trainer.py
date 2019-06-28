'''
Created on Jan 2, 2017

@author: A.Khateeb
'''

from mysql.connector import Error as sq_error
import mysql.connector as sq
from pre_processing import classic_tokenizer
from pre_processing import purifier

from nltk.probability import FreqDist


class Trainer():
    # Bring and fetch records from DB
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
    
    def select(self,table,category,limit = 1000, offset = 0):
        self.cursor.execute("SELECT Body FROM `{}` WHERE lower(`category`) like lower(\"{}\") LIMIT {} OFFSET {};".format(table,category,limit,offset))
        return self.cursor.fetchall()
            
    def countVect(self,article,cats):
        from sklearn.feature_extraction.text import CountVectorizer

        vec = CountVectorizer().fit(self.corpora)
        vector = vec.transform(article)
        
        print (u"Vector: [{}]".format(vector.toarray()))
        exit(0)
        
    def main(self):
        TABLE = "article"
        cats = ['Economy','Art','Climate','Crime','Health','Politics','Religion','Science','Sport','Tech'] 
    
        config = {"host":'localhost',"user":'python',"password":'0000',"db":'mdac'}
        self.db_connect(config)
        print (u"processing records")
        self.corpora = dict()
        for cat in cats:
            bag = dict()
            for article in self.select(TABLE,cat): # tryutn Tuple .. [0] is the result
                article = purifier.purify(article[0])
                words = classic_tokenizer.tokenize(article)
                bag = FreqDist(words)
                self.corpora.update({cat:bag})
            print (u"Words of Cat:[{}] are: ({})".format(cat,str(len(bag.values()))))

#         self.countVect(article,cats)
        
if __name__ == '__main__': 
    obj = Trainer()
    obj.main()