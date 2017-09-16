'''
Created on 16 Sep 2017

@author: Mathias Bucher
'''
from Tkinter import Frame
from VStyles import rootColor, getFrame, getButtonEntry
from model.ModelEntry import ModelEntry

class VOverview(Frame):
    '''
    classdocs
    '''
    name = "Overview"


    def __init__(self, parent, log, actions):
        '''
        Constructor
        '''
        Frame.__init__(self, parent)
        self.configure(bg=rootColor)
        self.log = log
        self.actions = actions
        self.sortedEntries = dict()
        self.log.add(self.log.Info, __file__, "init" )
        
    def show(self, entries):
        '''Displays the entries dict sorted by their keys'''
        currentRow = 0
        for k, v in entries.iteritems():
            self.sortedEntries[k] = getFrame(self)
            
            for e in v:
                but = getButtonEntry(self.sortedEntries[k], command=lambda n=e.name: self.entryClicked(n))
                but["text"] = e.name
            self.sortedEntries[k].grid(row=currentRow)
            currentRow += 1
    
    def entryClicked(self, entryName):
        '''This method is called when any showed entry is clicked'''
        self.log.add(self.log.Info, __file__, entryName + " clicked")
        
        if self.actions != None:
            if "showEntryOverviewAction" in self.actions:
                self.actions["showEntryOverviewAction"](entryName)
                
    def removeAll(self):
        '''Removes all showed entries'''
        for k, v in self.sortedEntries.iteritems():
            self.sortedEntries[k].destroy()
        self.sortedEntries = dict()