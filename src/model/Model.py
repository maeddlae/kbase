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
        self.db.hasEntry(entry)