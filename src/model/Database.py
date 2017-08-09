'''
Created on 9 Aug 2017

@author: Mathias Bucher
'''
import sqlite3
import os

class Database(object):
    '''
    This class represents the interface to the database. 
    '''
    path = "data.db"


    def __init__(self, log):
        '''
        Constructor
        '''
        self.log = log
        self.db = sqlite3.connect(self.path)
        
        if os.path.exists(self.path) == False:
            self.createTable()
        
        self.log.add(self.log.Info, __file__, "init" )
    
    def createTable(self):
        c = self.db.cursor()
        c.execute('''CREATE TABLE stocks (name text, description text, keywords text)''')
        c.execute("INSERT INTO stocks VALUES ('buildings', 'This is a building', 'Empire State')")
        self.db.commit()
        self.db.close()
        