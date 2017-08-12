'''
Created on 9 Aug 2017

@author: Mathias Bucher
'''
import sqlite3
from model.ModelEntry import ModelEntry

class Database(object):
    '''
    This class represents the interface to the database and implements some 
    search and add methods. 
    '''

    def __init__(self, log, path):
        '''
        Constructor
        '''        
        self.log = log        
        self.path = path                
        self.log.add(self.log.Info, __file__, "init with: " + self.path )
        
    def hasEntry(self, entry):
        '''Checks if an entry already exists. Uses the name for its check'''
        try:
            db = sqlite3.connect(self.path)
            cur = db.cursor()
            cur.execute("SELECT * FROM entries WHERE name = ?", (entry.name,))
            data=cur.fetchone()
            db.close()
            if data is None:
                return False
            else:
                return True
        except sqlite3.Error, e:
            self.log.add(self.log.Warning, __file__, "db error: " + e.message)
            return False

        
    def addEntry(self, entry):
        '''Adds the entry to the db'''
        #check if entry already exists
        if self.hasEntry(entry):
            self.log.add(self.log.Info, __file__, entry.name + " already exists")
            return

        # otherwise try to add the entry
        try:
            db = sqlite3.connect(self.path)
            c = db.cursor()
            s = self.getStringFromKeywords(entry.keywords)
            c.execute("INSERT INTO entries VALUES (?, ?, ?)", (entry.name, entry.description, s))
            db.commit()
            db.close()
            
        except sqlite3.Error, e:
            self.log.add(self.log.Warning, __file__, "db error: " + e.message)
        
    def updateEntry(self, e):
        '''Updates an existing entry in the db. Note that the name can not be changed with this method'''
        #check if entry does not exist
        if not self.hasEntry(e):
            self.log.add(self.log.Info, __file__, e.name + " does not exist")
            return

        # otherwise try to update the entry
        try:
            db = sqlite3.connect(self.path)
            c = db.cursor()
            s = self.getStringFromKeywords(e.keywords)
            c.execute('''UPDATE entries SET description=?, keywords=? WHERE name=?''', [e.description, s, e.name])
            db.commit()
            db.close()
            
        except sqlite3.Error, e:
            self.log.add(self.log.Warning, __file__, "db error: " + e.message)
    
    def getEntryByName(self, name):
        '''Searches an entry by name. Returns found entry or None, if not found'''
        e = None
        
        try:
            db = sqlite3.connect(self.path)
            db.row_factory = sqlite3.Row
            c = db.cursor()
            c.execute("SELECT * FROM entries WHERE name = ?", (name,))
            data=c.fetchone()
            db.close()
            
            if data is None:
                self.log.add(self.log.Warning, __file__, "entry with name = " + name + " not found" )
            else:
                e = self.getEntryFromRowObject( data )
                
        except sqlite3.Error, e:
            self.log.add(self.log.Warning, __file__, "get by name fail: " + e.message)
        
        return e
        
    def getEntryByKeyword(self, keyword):
        '''Searches an entry by keyword. Returns found entry or None, if not found'''
        e = None
        
        try:
            db = sqlite3.connect(self.path)
            db.row_factory = sqlite3.Row
            c = db.cursor()
            search = "%" + keyword + "%"
            c.execute("SELECT * FROM entries WHERE keywords LIKE ?", (search,))
            data=c.fetchone()
            db.close()
            
            if data is None:
                self.log.add(self.log.Warning, __file__, "entry with keyword = " + keyword + " not found" )
            else:
                e = self.getEntryFromRowObject( data )
                
        except sqlite3.Error, e:
            self.log.add(self.log.Warning, __file__, "get by keyword fail: " + e.message)
        
        return e
        
    def getEntryByDescription(self, word):
        '''Searches an entry by description. Returns found entry or None, if not found'''
        e = None
        
        try:
            db = sqlite3.connect(self.path)
            db.row_factory = sqlite3.Row
            c = db.cursor()
            search = "%" + word + "%"
            c.execute("SELECT * FROM entries WHERE description LIKE ?", (search,))
            data=c.fetchone()
            db.close()
            
            if data is None:
                self.log.add(self.log.Warning, __file__, "entry with word = " + word + " not found" )
            else:
                e = self.getEntryFromRowObject( data )
                
        except sqlite3.Error, e:
            self.log.add(self.log.Warning, __file__, "get by word fail: " + e.message)
        
        return e
    
    def getStringFromKeywords(self, keywords):
        '''Puts all elements of keywords into a string, separated by comma'''
        s = ""
        first = True
        for k in keywords:
            if first:
                first = False
            else:
                s += ","
            s += k
                    
        return s
    
    def getKeywordsFromString(self, string):
        '''Returns all comma separated keywords in a list'''
        return string.split(",")
    
    def getEntryFromRowObject(self, data):
        '''Makes an entry of a row object. Sql db extracts usually row objects'''
        if data == None:
            return None
        
        s = data["name"].encode("ascii")
        e = ModelEntry(self.log, s)
        s = data["description"].encode("ascii")
        e.description = s
        s = data["keywords"].encode("ascii")
        e.keywords = self.getKeywordsFromString(s)   
        
        return e
        