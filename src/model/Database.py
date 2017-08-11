'''
Created on 9 Aug 2017

@author: Mathias Bucher
'''
import sqlite3
import os
from model.ModelEntry import ModelEntry

class Database(object):
    '''
    This class represents the interface to the database. 
    '''


    def __init__(self, log, path):
        '''
        Constructor
        '''
        self.log = log
        
        self.path = path
        self.db = sqlite3.connect(self.path)
                
        self.log.add(self.log.Info, __file__, "init with: " + self.path )
        
    def __del__(self):
        self.db.close
        
    def addEntry(self, entry):
        "Adds the entry to the db"
        #todo: what if entry already exists? update entry?
        try:
            c = self.db.cursor()
            c.execute("INSERT INTO entries VALUES (?, ?, 'Yamaha,Kawasaki')", (entry.name, entry.description))
            self.db.commit()
            self.db.close()
            
        except sqlite3.Error, e:
            self.log.add(self.log.Warning, __file__, "db error: " + e)
        
        
    def getEntryByName(self, name):
        #todo
        e = None
        
        try:
            self.db.row_factory = sqlite3.Row
            c = self.db.cursor()
            c.execute("SELECT * FROM entries WHERE name = ?", (name,))
            
            data=c.fetchone()
            
            if data is None:
                self.log.add(self.log.Warning, __file__, "entry with name = ? not found"%name )
            else:
                #e = ModelEntry(self.log)
                #e.name = data["name"]
                #e.description = data["description"]
               # e.keywords = data["keywords"]
               pass
                
        except sqlite3.Error, e:
            self.log.add(self.log.Warning, __file__, "add entry into db failed" )
        
        return e