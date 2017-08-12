'''
Created on 24 Jul 2017

@author: Mathias Bucher
'''
from model.ModelEntry import ModelEntry
from model.Database import Database

class Model():
    '''
    classdocs
    '''

    def __init__(self, log):
        '''
        Constructor
        '''
        self.log = log
        self.db = Database(self.log,"D:\Mathias Bucher\Documents\others\Basteln\Python\kbase\data\data.db")
        self.log.add(self.log.Info, __file__, "init" )
        
        
    def getEntry(self, word):        
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