'''
Created on 19 Aug 2017

@author: Mathias Bucher
'''
from VEntry import VEntry
from VSearch import VSearch
from VOverview import VOverview
from ttk import Notebook
from VStyles import styleNotebook

class VTab(Notebook):
    '''
    Holds overview, search and entries in tabs.
    '''


    def __init__(self, parent, log, actions):
        '''
        Constructor
        '''
        Notebook.__init__(self, parent)
        self = styleNotebook(self)
        
        self.log = log
        self.actions = actions
        self.vsearch=None
        self.ventries = {}
        self.tabIds = {}
        self.vsearchDrawn = False
        self.overview = None
        self.bind("<<NotebookTabChanged>>", self.tabChanged)
        self.log.add(self.log.Info, __file__, "init" )
        
    def setOverview(self, entries):
        '''Shows the overview of all entries'''
        if self.overview == None:
            self.overview = VOverview(log=self.log, parent=self, actions=self.actions)
            self.add(self.overview, text=self.overview.name)
        else:
            self.overview.removeAll()
        self.overview.show(entries)
        self.select(self.getTabId(self.overview))
        self.log.add(self.log.Info, __file__, "draw overview tab" )        
        
    def setSearch(self, results):
        '''Adds the search view or updates it, if it already exists'''
        # if it is the first time a search is startet..
        if self.vsearch == None:
            # ..then make search object and add it
            self.vsearch = VSearch(log=self.log, parent=self, actions=self.actions)
            self.add(self.vsearch, text=self.vsearch.name)
            self.vsearchDrawn = True
        else:
            # ..otherwise update the existing one
            self.vsearch.removeOldResults()
            
        self.vsearch.drawSearchResults(results)
        self.select(self.getTabId(self.vsearch))
        self.log.add(self.log.Info, __file__, "draw search tab" )
        
    def addEntry(self, entry):
        '''Adds an entry as a tab'''
        # add only if entry does not exist
        if not entry.name in self.ventries:
            self.ventries[entry.name] = VEntry(parent=self, log=self.log, actions=self.actions)
            self.add(self.ventries[entry.name], text=entry.name)
            self.ventries[entry.name].drawEntry(entry)
        
        # select this new entry. Must be done by tabid
        self.select(self.getTabId(self.ventries[entry.name]))
        self.log.add(self.log.Info, __file__, "add " + entry.name + " tab" )
        
    def removeEntry(self, entry):
        '''Removes an existing entry'''
        if entry.name not in self.ventries:
            return
        
        tabId = self.getTabId(self.ventries[entry.name])
        self.forget(tabId)
        self.ventries[entry.name].destroy()
        del self.ventries[entry.name]
        self.log.add(self.log.Info, __file__, "removed " + entry.name + " tab" )
        
    def removeSearch(self):
        '''Removes the opened search if there is one'''
        if not self.vsearchDrawn:
            return
        
        tabId = self.getTabId(self.vsearch)
        self.forget(tabId)
        self.vsearch.destroy()
        self.vsearch = None
        self.vsearchDrawn = False
        self.log.add(self.log.Info, __file__, "search removed" )
        
    def getTabId(self, frame):
        '''Returns the tab id of the frame'''
        return self.children[frame._name]
    
    def hasTabs(self):
        '''Returns true if there is at least one active tab'''
        return self.tabs().__len__() != 0
    
    def getActiveTabId(self):
        '''Returns the tab id of the currently active tab. Tab id is 
        a unique number, which identifies the widget. Tab id is stored 
        in _name field of every widget'''
        fullId = self.select()
        splitted = fullId.rsplit(".", 1)
        if splitted.__len__() == 1:
            tabId = splitted[0]
        else:
            tabId = splitted[1]
        return tabId
    
    def getNameOfActiveTab(self):
        '''Returns the name of the currently active tab'''
        tabid = self.getActiveTabId()
        
        if tabid == None:
            return None
        
        # check if active tab is overview
        if self.overview != None:
            if tabid == self.overview._name:
                return self.overview.name
        
        # check if active tab is vsearch
        if self.vsearch != None:
            if tabid == self.vsearch._name:
                return self.vsearch.name
        
        # check if is entry
        for e in self.ventries.values():
            if tabid == e._name:
                return e.getName()
    
    def tabChanged(self, _event):
        '''Is called every time the active tab changes'''
        self.log.add(self.log.Info, __file__, "tab changed" )
        
        nameOfActiveTab = self.getNameOfActiveTab()
        
        if self.actions != None:
            if "tabChangeAction" in self.actions:
                self.actions["tabChangeAction"](nameOfActiveTab)
        