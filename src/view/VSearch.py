'''
Created on 12 Aug 2017

@author: Mathias Bucher
'''
from Tkinter import *

class VSearch(Frame):
    '''
    Shows search results
    '''

    def __init__(self, parent, log, actions):
        '''
        Constructor
        '''
        Frame.__init__(self, parent)
        self.log = log
        self.actions = actions
        self.buttonName = []
        self.buttonTag = []
        self.buttonDescription = []
        self.log.add(self.log.Info, __file__, "init" )
        
    def removeOldResults(self):
        '''Removes the old results'''
        self.labelName.destroy()
        self.frameName.destroy()
        self.labelTag.destroy()
        self.frameTag.destroy()
        self.labelDescription.destroy()
        self.frameDescription.destroy()
        
        self.buttonName = []
        self.buttonTag = []
        self.buttonDescription = []
        
    def drawSearchResults(self, results):
        '''Draws the found search results sorted by name, tag and 
        description match'''
        self.labelName = Label(self)
        self.labelName["text"] = "found by name:"
        self.labelName.grid(row=0, sticky=W)
        
        self.frameName = Frame(self)
        for i, e in enumerate(results["name"]):
            but = Button(self.frameName, command=lambda n=e.name: self.buttonEntryClicked(n))
            self.buttonName.append(but)
            self.buttonName[i].grid(row=1, column=i, sticky=W)
            self.buttonName[i]["text"] = e.name
        self.frameName.grid(sticky=W)
        
        self.labelTag = Label(self)
        self.labelTag["text"] = "found by tag:"
        self.labelTag.grid(row=2, sticky=W)
        
        self.frameTag = Frame(self)
        for i, e in enumerate(results["tag"]):
            but = Button(self.frameTag, command=lambda n=e.name: self.buttonEntryClicked(n))
            self.buttonTag.append(but)
            self.buttonTag[i].grid(row=3, column=i, sticky=W)
            self.buttonTag[i]["text"] = e.name
        self.frameTag.grid(sticky=W)
        
        self.labelDescription = Label(self)
        self.labelDescription["text"] = "found by description:"
        self.labelDescription.grid(row=4, sticky=W)
        
        self.frameDescription = Frame(self)
        for i, e in enumerate(results["description"]):
            but = Button(self.frameDescription, command=lambda n=e.name: self.buttonEntryClicked(n))
            self.buttonDescription.append(but)            
            self.buttonDescription[i].grid(row=5, column=i, sticky=W)
            self.buttonDescription[i]["text"] = e.name
        self.frameDescription.grid(sticky=W)
            
    def buttonEntryClicked(self, entryName):
        '''This method is called when any showed entry is clicked'''
        self.log.add(self.log.Info, __file__, entryName + " clicked")
        
        if self.actions != None:
            if "showEntryAction" in self.actions:
                self.actions["showEntryAction"](entryName)