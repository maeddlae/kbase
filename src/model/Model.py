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
        
        
    def getEntry(self, word):        
        '''Searches an entry in the db by name, keyword or description in sequence. 
        Returns only the first match'''
        # find by name
        foundEntry = self.db.getEntryByName(word)
        
        # find by keyword
        if foundEntry == None:
            foundEntry = self.db.getEntryByKeyword(word)
        
        # find by description
        if foundEntry == None:
            foundEntry = self.db.getEntryByDescription(word)
            
        if foundEntry != None:
            self.log.add(self.log.Info, __file__, "entry found" )
        else:
            self.log.add(self.log.Info, __file__, "entry not found" )
            
        return foundEntry
    
    def updateNameOfEntry(self, entry, newName):
        self.db.updateNameOfEntry(entry, newName)
    
    def updateContentOfEntry(self, entry):
        self.db.updateEntry(entry)
        
    def addEntry(self, entry):
        self.db.addEntry(entry)
        
    def hasEntry(self, entry):
        self.db.hasEntry(entry)