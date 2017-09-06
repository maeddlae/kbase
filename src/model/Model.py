'''
Created on 24 Jul 2017

@author: Mathias Bucher
'''
from model.Database import Database

class Model():
    '''
    classdocs
    '''

    def __init__(self, log, path):
        '''
        Constructor
        '''
        self.log = log
        self.db = Database(self.log, path)
        self.log.add(self.log.Info, __file__, "init" )
        self.openedEntries = []
        self.foundEntries = {"name" : [],
                            "keyword" : [],
                            "description" : []}
        self.currentEntry = None
        
    def setDatabase(self, path):
        '''Changes the active database'''
        self.db = Database(self.log, path)
    
    def getEntries(self, word):        
        '''Searches entries in the db by name, keyword or description in sequence. 
        Returns all matches in a dict, with keys = name, keyword and description. 
        The key says according to which characteristic the entry has been found. 
        The entries are then saved as a list: '''
        # get all entries
        byName = self.db.getEntriesByName(word)
        byKeyword = self.db.getEntriesByKeyword(word)
        byDescription = self.db.getEntriesByDescription(word)
        
        
        found = {"name" : list(byName),
                 "keyword" : list(byKeyword),
                 "description" : list(byDescription)}
        self.foundEntries = found
        
        self.log.add(self.log.Info, __file__, "found " + str(found["name"].__len__()) + " by name" )
        self.log.add(self.log.Info, __file__, "found " + str(found["keyword"].__len__()) + " by keyword" )
        self.log.add(self.log.Info, __file__, "found " + str(found["description"].__len__()) + " by description" )
            
        return found
    
    def updateNameOfEntry(self, entry, newName):
        self.db.updateNameOfEntry(entry, newName)
    
    def updateContentOfEntry(self, entry):
        self.db.updateEntry(entry)
        
    def addEntry(self, entry):
        self.db.addEntry(entry)
        
    def hasEntry(self, entry):
        return self.db.hasEntry(entry)
        
    def removeEntry(self, entry):
        self.db.removeEntry(entry)
        
    def getOpenedEntry(self, entryName):
        '''Return entry with entryName, that has been openend'''
        for e in self.openedEntries:
            if e.name == entryName:
                return e
        return None
    
    def getFoundEntry(self, entryName):
        '''Returns the entry with entryName, that has been found 
        previously'''
        for e in self.foundEntries["name"]:
            if e.name == entryName:
                return e
        for e in self.foundEntries["description"]:
            if e.name == entryName:
                return e
        for e in self.foundEntries["keyword"]:
            if e.name == entryName:
                return e
        return None