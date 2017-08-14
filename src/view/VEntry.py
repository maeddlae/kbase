'''
Created on 12 Aug 2017

@author: Mathias Bucher
'''
from Tkinter import *

class VEntry(Frame):
    '''
    Shows an entry and allows changes on it.
    '''

    def __init__(self, root, log, actions):
        '''
        Constructor
        '''
        Frame.__init__(self, root)
        self.log = log
        self.log.add(self.log.Info, __file__, "init" )
        self.actions = actions
        
            
    def drawEntry(self, entry):
        '''Draws an entry. If the entry is None, it does nothing'''
        if entry != None:
            self.name = Text(self, height=1, width=20, font=("Helvetica", 15, "bold"))
            self.name.insert(END, entry.name)
            self.name.grid(row=1, column=0, sticky=W)
            self.name.bind( "<Return>", self.returnPressedAtName)
            
            self.description = Text(self, height=6, font=("Helvetica", 10))
            self.description.insert(END, entry.description)
            self.description.grid(row=2, sticky=W)
            self.description.bind( "<Return>", self.returnPressedAtDescription)
            
            self.keywords = Text(self, height=2, font=("Helvetica", 10))
            s = entry.getStringFromKeywords(entry.keywords)
            self.keywords.insert(END, s)
            self.keywords.grid(row=3, sticky=W)
            self.keywords.bind( "<Return>", self.returnPressedAtKeywords)
            
            self.log.add(self.log.Info, __file__, "entry " + entry.name + " drawn" )

    def returnPressedAtName(self, event):
        '''Is called when user hits Return key while writing in name field'''
        t = self.name.get("1.0", 'end-1c')
        self.log.add(self.log.Info, __file__, "name change: " + t)
        
        if self.actions != None:
            if "changeNameAction" in self.actions:
                self.actions["changeNameAction"](t)
        
    def returnPressedAtDescription(self, event):
        '''Is called when user hits Return key while writing in description field'''
        t = self.description.get("1.0", 'end-1c')
        self.log.add(self.log.Info, __file__, "description change: " + t)
                
        if self.actions != None:
            if "changeDescriptionAction" in self.actions:
                self.actions["changeDescriptionAction"](t)
    
    def returnPressedAtKeywords(self, event):
        '''Is called when user hits Return key while writing in keywords field'''
        t = self.keywords.get("1.0", 'end-1c')
        self.log.add(self.log.Info, __file__, "keywords change: " + t )
                
        if self.actions != None:
            if "changeKeywordsAction" in self.actions:
                self.actions["changeKeywordsAction"](t)
