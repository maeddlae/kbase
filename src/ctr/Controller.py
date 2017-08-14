'''
Created on 24 Jul 2017

@author: Mathias Bucher
'''
from ctr.Log import Log
from model.Model import Model
from view.View import View


class Controller():
    dbPath = "D:\Mathias Bucher\Documents\others\Basteln\Python\kbase\data\data.db"

    def __init__(self):
        '''Constructor'''
        self.actions = {"menuGoClicked" : self.buttonGoAction,
                        "changeNameAction" : self.entryNameChangeAction,
                        "changeDescriptionAction" : self.entryDescriptionChangeAction,
                        "changeKeywordsAction" : self.entryKeywordChangeAction }
        self.log = Log("log.txt")
        self.view = View(self.log, self.actions)
        self.model = Model(self.log, self.dbPath)
        
        self.log.add(self.log.Info, __file__, "init" )
        
    def run(self):        
        self.view.run()
        
    def buttonGoAction(self, keyword):
        self.log.add(self.log.Info, __file__, "search for : " + keyword)
        
        self.currentEntry = self.model.getEntry(keyword)
        
        if self.currentEntry != None:
            self.view.drawEntry(self.currentEntry)
        else:
            self.view.drawSearch()
            
    def entryNameChangeAction(self, newName):
        '''Simply calls update name from model with current entry'''
        self.model.updateNameOfEntry(self.currentEntry, newName)
        self.currentEntry.name = newName

    def entryDescriptionChangeAction(self, newDescription):
        '''Updates current entry and calls update method from model'''
        self.currentEntry.description = newDescription
        self.model.updateContentOfEntry(self.currentEntry)

    def entryKeywordChangeAction(self, newKeywords):
        '''Updates current entry and calls update method from model'''
        k = self.currentEntry.getKeywordsFromString(newKeywords)
        self.currentEntry.keywords = k
        self.model.updateContentOfEntry(self.currentEntry)        
