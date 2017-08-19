'''
Created on 19 Aug 2017

@author: Mathias Bucher
'''
from Tkinter import *
from VEntry import VEntry
from VSearch import VSearch
from ttk import Notebook

class VTab(Notebook):
    '''
    Holds overview, search and entries in tabs.
    '''


    def __init__(self, parent, log, actions):
        '''
        Constructor
        '''
        Notebook.__init__(self, parent)
        self.log = log
        self.log.add(self.log.Info, __file__, "init" )
        self.actions = actions
        self.vsearch=VSearch(log=self.log, parent=self, actions=self.actions)
        self.ventries = {}
        self.tabIds = {}
        self.vsearchDrawn = False
        
    def setSearch(self, results):
        '''Adds the search view or updates it, if it already exists'''
        # if it is the first time a search is startet..
        if not self.vsearchDrawn:
            # ..then make search object and add it
            self.add(self.vsearch, text="Search")
            self.vsearchDrawn = True
        else:
            # ..otherwise update the existing one
            self.vsearch.removeOldResults()
            
        self.vsearch.drawSearchResults(results)
        self.select(self.getTabId(self.vsearch))
        
    def addEntry(self, entry):
        '''Adds an entry as a tab'''
        # add only if entry does not exist
        if not entry.name in self.ventries:
            self.ventries[entry.name] = VEntry(parent=self, log=self.log, actions=self.actions)
            self.add(self.ventries[entry.name], text=entry.name)
            self.ventries[entry.name].drawEntry(entry)
        
        # select this new entry. Must be done by tabid
        self.select(self.getTabId(self.ventries[entry.name]))
        
    def removeEntry(self, entry):
        '''Removes an existing entry'''
        if entry.name not in self.ventries:
            return
        
        tabId = self.getTabId(self.ventries[entry.name])
        self.forget(tabId)
        self.ventries[entry.name].destroy()
        del self.ventries[entry.name]
        
    def getTabId(self, frame):
        '''Returns the tab id of the frame'''
        return self.children[frame._name]
        