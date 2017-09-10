'''
Created on 9 Aug 2017

@author: Mathias Bucher
'''
import sqlite3
import os
from model.ModelEntry import ModelEntry
from model.FileHandle import FileHandle

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
        
        # create empty database if not already exists
        if not os.path.exists(self.path):
            db = sqlite3.connect(self.path)
            db.execute("CREATE TABLE entries(name TEXT, description TEXT, tags BLOB, images BLOB, files BLOB)")
            db.commit()
            db.close()
        
        self.fileHandle = FileHandle(self.log)
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
            s = buffer(self.fileHandle.getStreamFromFiles(entry.tags))
            p = buffer(self.fileHandle.getStreamFromFiles(entry.images))
            f = buffer(self.fileHandle.getStreamFromFiles(entry.files))
            c.execute("INSERT INTO entries VALUES (?, ?, ?, ?, ?)", (entry.name, entry.description, s, p, f))
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
            s = buffer(self.fileHandle.getStreamFromFiles(e.tags))
            img = buffer(self.fileHandle.getStreamFromFiles(e.images))
            fil = buffer(self.fileHandle.getStreamFromFiles(e.files))
            c.execute('''UPDATE entries SET description=?, tags=?, images=?, files=? WHERE name=?''', [e.description, s, img, fil, e.name])
            db.commit()
            db.close()
            
        except sqlite3.Error, e:
            self.log.add(self.log.Warning, __file__, "db error: " + e.message)
    
    def updateNameOfEntry(self, e, newName):
        '''Changes the name of an existing entry'''
        #check if entry does not exist
        if not self.hasEntry(e):
            self.log.add(self.log.Info, __file__, e.name + " does not exist")
            return

        # otherwise try to change the name
        try:
            db = sqlite3.connect(self.path)
            db.row_factory = sqlite3.Row
            c = db.cursor()
            c.execute("DELETE FROM entries WHERE name=?", [e.name])
            e.name = newName
            s = buffer(self.fileHandle.getStreamFromFiles(e.tags))
            img = buffer(self.fileHandle.getStreamFromFiles(e.images))
            fil = buffer(self.fileHandle.getStreamFromFiles(e.files))
            c.execute("INSERT INTO entries VALUES (?, ?, ?, ?, ?)", [e.name, e.description, s, img, fil])
            db.commit()
            db.close()
            
        except sqlite3.Error, e:
            self.log.add(self.log.Warning, __file__, "db error: " + e.message)
    
    def getEntriesByName(self, name):
        '''Searches entries by name. Returns a list of found entries'''
        found = []
        
        try:
            db = sqlite3.connect(self.path)
            db.row_factory = sqlite3.Row
            c = db.cursor()
            search = "%" + name + "%"
            c.execute("SELECT * FROM entries WHERE name LIKE ?", (search,))
            data=c.fetchall()
            db.close()
            
            if data.__len__() == 0:
                self.log.add(self.log.Warning, __file__, "no entry named " + name + " found" )
            else:
                for e in data:
                    found.append(self.getEntryFromRowObject(e))
                
        except sqlite3.Error, e:
            self.log.add(self.log.Warning, __file__, "get by name fail: " + e.message)
        
        return found
    
    def getEntriesByDescription(self, description):
        '''Searches entries by description. Returns a list of found entries'''
        found = []
        
        try:
            db = sqlite3.connect(self.path)
            db.row_factory = sqlite3.Row
            c = db.cursor()
            search = "%" + description + "%"
            c.execute("SELECT * FROM entries WHERE description LIKE ?", (search,))
            data=c.fetchall()
            db.close()
            
            if data.__len__() == 0:
                self.log.add(self.log.Warning, __file__, "no entry with " + description + " found" )
            else:
                for e in data:
                    found.append(self.getEntryFromRowObject(e))
                
        except sqlite3.Error, e:
            self.log.add(self.log.Warning, __file__, "get by description fail: " + e.message)
        
        return found
    
    def getEntriesByTag(self, tag):
        '''Searches entries by tag. Returns a list of found entries'''
        found = []
        
        try:
            db = sqlite3.connect(self.path)
            db.row_factory = sqlite3.Row
            c = db.cursor()
            search = "%" + tag + "%"
            c.execute("SELECT * FROM entries WHERE tags LIKE ?", (search,))
            data=c.fetchall()
            db.close()
            
            if data.__len__() == 0:
                self.log.add(self.log.Warning, __file__, "no entry with tag: " + tag + " found" )
            else:
                for e in data:
                    found.append(self.getEntryFromRowObject(e))
                
        except sqlite3.Error, e:
            self.log.add(self.log.Warning, __file__, "get by tag fail: " + e.message)
        
        return found
    
    def getEntryFromRowObject(self, data):
        '''Makes an entry of a row object. Sql db extracts usually row objects'''
        if data == None:
            return None
        
        s = data["name"].encode("ascii")
        e = ModelEntry(self.log, s)
        s = data["description"].encode("ascii")
        e.description = s
        e.tags = self.fileHandle.getFilesFromStream(bytearray(data["tags"]))
        e.images = self.fileHandle.getFilesFromStream(bytearray(data["images"]))
        e.files = self.fileHandle.getFilesFromStream(bytearray(data["files"]))
        return e
    
    def removeEntry(self, entry):
        '''Removes an entry (forever) of the database'''
        try:
            db = sqlite3.connect(self.path)
            c = db.cursor()
            search = "%" + entry.name + "%"
            c.execute("DELETE FROM entries WHERE name LIKE ?", (search,))
            db.commit()
            db.close()
            
        except sqlite3.Error, e:
            self.log.add(self.log.Warning, __file__, "get by tag fail: " + e.message)
        
        