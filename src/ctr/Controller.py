'''
Created on 24 Jul 2017

@author: Mathias Bucher
'''
from ctr.Log import Log
from model.Model import Model
from model.ModelEntry import ModelEntry
from view.View import View
from model.ConfigFile import ConfigFile


class Controller():
    
    def __init__(self, log, config):
        '''Constructor'''
        self.actions = {"searchAction" : self.searchAction,
                        "changeNameAction" : self.entryNameChangeAction,
                        "newAction" : self.newEntryAction,
                        "changeDescriptionAction" : self.entryDescriptionChangeAction,
                        "changeKeywordsAction" : self.entryKeywordChangeAction,
                        "showEntryAction" : self.entryClickedInVSearch,
                        "closedAction" : self.closeTabAction,
                        "tabChangeAction" : self.tabChangeAction,
                        "deleteAction" : self.deleteEntryAction}
        if log != None:
            self.log = log
        else:
            self.log = Log("log.txt")
        
        self.config = ConfigFile( self.log, config )
        self.dbPath = self.config.getValue("databasepath")
        self.view = View(self.log, self.dbPath, self.actions)
        self.model = Model(self.log, self.dbPath)
        self.isSearchActive = False
        
        self.log.add(self.log.Info, __file__, "init" )
        
    def run(self):        
        self.view.run()
        
    def searchAction(self, keyword):
        self.log.add(self.log.Info, __file__, "search for : " + keyword)
        results = self.model.getEntries(keyword)
        self.view.drawSearch(results)
            
    def entryNameChangeAction(self, newName):
        '''Simply calls update name from model with current entry'''
        self.view.removeEntry(self.currentEntry)
        self.model.updateNameOfEntry(self.currentEntry, newName)
        self.currentEntry.name = newName
        self.view.drawEntry(self.currentEntry)

    def entryDescriptionChangeAction(self, newDescription):
        '''Updates current entry and calls update method from model'''
        self.currentEntry.description = newDescription
        self.model.updateContentOfEntry(self.currentEntry)
        self.view.drawEntry(self.currentEntry)

    def entryKeywordChangeAction(self, newKeywords):
        '''Updates current entry and calls update method from model'''
        k = self.currentEntry.getKeywordsFromString(newKeywords)
        self.currentEntry.keywords = k
        self.model.updateContentOfEntry(self.currentEntry)  
        self.view.drawEntry(self.currentEntry) 
        
    def newEntryAction(self):
        '''Adds a new entry'''
        newNameText = "enter name"
        self.currentEntry = ModelEntry(self.log, newNameText)
        i = 0
        
        while self.model.hasEntry(self.currentEntry):
            i += 1
            newName = newNameText + str(i)
            self.currentEntry.name = newName
        
        self.model.activeEntries.append(self.currentEntry)
        self.model.addEntry(self.currentEntry)
        self.view.drawEntry(self.currentEntry)
        
    def entryClickedInVSearch(self, entry):
        '''Shows the clicked entry'''
        self.currentEntry = entry
        self.model.activeEntries.append(entry)
        self.view.drawEntry(entry)
        
    def closeTabAction(self):
        '''Closes the currently active tab'''
        if self.isSearchActive:
            self.view.removeSearch()
            self.currentEntry = None
        else:
            self.model.activeEntries.remove(self.currentEntry)
            self.view.removeEntry(self.currentEntry)
        
    def tabChangeAction(self, activeTabName, isSearchActive):
        '''Is called when tab focus changes'''
        # only do something when has a valid name
        if activeTabName != None:
            for e in self.model.activeEntries:
                if activeTabName == e.name:
                    self.currentEntry = e
                    self.view.setDeleteButton(True)
                    
        self.isSearchActive = isSearchActive
        if isSearchActive == True:
            self.view.setDeleteButton(False)
            
    def deleteEntryAction(self):
        '''Deletes the currently active entry'''
        self.model.removeEntry(self.currentEntry)
        self.view.removeEntry(self.currentEntry)
        