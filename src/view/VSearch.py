'''
Created on 12 Aug 2017

@author: Mathias Bucher
'''
from Tkinter import *

class VSearch(Frame):
    '''
    Shows search results
    '''


    def __init__(self, root, log, actions):
        '''
        Constructor
        '''
        Frame.__init__(self, root)
        self.log = log
        self.actions = actions
        self.log.add(self.log.Info, __file__, "init" )
        
    def drawSearchResults(self, results):
        '''Draws the found search results sorted by name, keyword and 
        description match'''
        
        self.labelName = Label(self)
        self.labelName["text"] = "found by name:"
        self.labelName.grid(row=1, sticky=W)
        
        self.frameName = Frame(self)
        self.buttonName = []
        for i, e in enumerate(results["name"]):
            but = Button(self.frameName, command=lambda n=e: self.buttonEntryClicked(n))
            self.buttonName.append(but)
            self.buttonName[i].grid(row=2, column=i, sticky=W)
            self.buttonName[i]["text"] = e.name
        self.frameName.grid(sticky=W)
        
        self.labelKeyword = Label(self)
        self.labelKeyword["text"] = "found by keyword:"
        self.labelKeyword.grid(row=3, sticky=W)
        
        self.frameKeyword = Frame(self)
        self.buttonKeyword = []
        for i, e in enumerate(results["keyword"]):
            but = Button(self.frameKeyword, command=lambda n=e: self.buttonEntryClicked(n))
            self.buttonKeyword.append(but)
            self.buttonKeyword[i].grid(row=4, column=i, sticky=W)
            self.buttonKeyword[i]["text"] = e.name
        self.frameKeyword.grid(sticky=W)
        
        self.labelDescription = Label(self)
        self.labelDescription["text"] = "found by description:"
        self.labelDescription.grid(row=5, sticky=W)
        
        self.frameDescription = Frame(self)
        self.buttonDescription = []
        for i, e in enumerate(results["description"]):
            but = Button(self.frameDescription, command=lambda n=e: self.buttonEntryClicked(n))
            self.buttonDescription.append(but)            
            self.buttonDescription[i].grid(row=6, column=i, sticky=W)
            self.buttonDescription[i]["text"] = e.name
        self.frameDescription.grid(sticky=W)
            
    def buttonEntryClicked(self, entry):
        '''This method is called when any showed entry is clicked'''
        self.log.add(self.log.Info, __file__, entry.name + " clicked")
        
        if self.actions != None:
            if "showEntryAction" in self.actions:
                self.actions["showEntryAction"](entry)