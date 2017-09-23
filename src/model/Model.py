'''
Created on 24 Jul 2017

@author: Mathias Bucher
'''
from model.Database import Database
from string import ascii_lowercase
from collections import OrderedDict

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
        self.openedEntries = [] # contains all entries, that are currently opened
        self.foundEntries = {"name" : [],
                            "tag" : [],
                            "description" : []} # contains all entries, that have been found
        self.currentEntry = None
        
    def setDatabase(self, path):
        '''Changes the active database'''
        self.db = Database(self.log, path)
        
    def getAllEntriesSorted(self):
        '''Returns all entries alphabetically sorted by name'''
        # get all entries from db
        entries = self.db.getEntriesByName("")
        
        s = OrderedDict()
        for e in entries:
            if not e.name[0] in s:
                s[e.name[0]] = list()
            s[e.name[0]].append(e)
            
        # sort by key
        sortedByKey = OrderedDict()
        key = s.keys()
        key.sort()
        for k in key:
            sortedByKey[k] = s[k]
        
        return sortedByKey
    
    def getEntries(self, word):        
        '''Searches entries in the db by name, tag or description in sequence. 
        Returns all matches in a dict, with keys = name, tag and description. 
        The key says according to which characteristic the entry has been found. 
        The entries are then saved as a list: '''
        # get all entries
        byName = self.db.getEntriesByName(word)
        byTag = self.db.getEntriesByTag(word)
        byDescription = self.db.getEntriesByDescription(word)
        
        # make sure every entry is showed only once
        for ed in byDescription:
            for et in byTag:
                if ed.name == et.name:
                    byDescription.remove(ed)
        for et in byTag:
            for en in byName:
                if et.name == en.name:
                    byTag.remove(et)
        
        found = {"name" : list(byName),
                 "tag" : list(byTag),
                 "description" : list(byDescription)}
        self.foundEntries = found
        
        self.log.add(self.log.Info, __file__, "found " + str(found["name"].__len__()) + " by name" )
        self.log.add(self.log.Info, __file__, "found " + str(found["tag"].__len__()) + " by tag" )
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
        for e in self.foundEntries["tag"]:
            if e.name == entryName:
                return e
        return None
    
    def getEntryByName(self, entryName):
        '''Returns the entry from database, whose name is entryName literally. Returns None if 
        entry does not exist'''
        entries = self.db.getEntriesByName(entryName)
        
        if entries.__len__() != 1:
            return None
        
        if entries[0].name != entryName:
            return None
        
        return entries[0]