'''
Created on 12 Aug 2017

@author: Mathias Bucher
'''
from Tkinter import *

class VEntry(Frame):
    '''
    Shows an entry and allows changes on it.
    '''
    width10=50
    width15=32

    def __init__(self, parent, log, actions):
        '''
        Constructor
        '''
        Frame.__init__(self, parent)
        self.log = log
        self.actions = actions
        self.log.add(self.log.Info, __file__, "init" )
            
    def drawEntry(self, entry):
        '''Draws an entry. If the entry is None, it does nothing'''
        if entry != None:
            self.name = Text(self, height=1, width=self.width15, font=("Helvetica", 15, "bold"))
            self.name.insert(END, entry.name)
            self.name.grid(row=0, column=0, sticky=W)
            self.name.bind( "<Return>", self.returnPressedAtName)
            
            self.description = Text(self, height=6, width=self.width10, font=("Helvetica", 10))
            self.description.insert(END, entry.description)
            self.description.grid(row=1, column=0, sticky=W)
            self.description.bind( "<Return>", self.returnPressedAtDescription)
            
            descScrollbar = Scrollbar(self, command=self.description.yview)
            descScrollbar.grid(row=1, column=1, sticky=W)
            self.description['yscrollcommand'] = descScrollbar.set
            
            self.keywords = Text(self, height=2, width=self.width10, font=("Helvetica", 10))
            s = entry.getStringFromKeywords(entry.keywords)
            self.keywords.insert(END, s)
            self.keywords.grid(row=2, sticky=W)
            self.keywords.bind( "<Return>", self.returnPressedAtKeywords)
            
            keyScrollbar = Scrollbar(self, command=self.keywords.yview)
            keyScrollbar.grid(row=2, column=1, sticky=W)
            self.keywords['yscrollcommand'] = keyScrollbar.set
            
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
