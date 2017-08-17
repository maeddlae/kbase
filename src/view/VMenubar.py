'''
Created on 17 Aug 2017

@author: Mathias Bucher
'''
from Tkinter import *

class VMenubar(Frame):
    '''
    Draws and handles the menubar
    '''


    def __init__(self, root, log, actions):
        '''
        Constructor
        '''
        Frame.__init__(self, root)
        self.log = log
        self.log.add(self.log.Info, __file__, "init" )
        self.actions = actions
        
    def draw(self):
        '''Draws the menu bar at the top of the window'''
        self.entrySearchText = StringVar()
        self.entrySearch = Entry(self)
        self.entrySearch["textvariable"] = self.entrySearchText
        self.entrySearchText.set("...")
        self.entrySearch.grid(row=0, column=0, sticky=W)
        self.entrySearch.bind( "<Return>", self.returnPressedAtSearch)
        
        self.buttonGo = Button(self)
        self.buttonGo.grid(row=0, column=1, sticky=W)
        self.buttonGo["text"] = "go"
        self.buttonGo["command"] = self.buttonGoClicked
        
        self.buttonNew = Button(self)
        self.buttonNew.grid(row=0, column=2, sticky=W)
        self.buttonNew["text"] = "new"
        self.buttonNew["command"] = self.buttonNewClicked
    
    def buttonGoClicked(self):
        t = self.entrySearchText.get()
        self.log.add(self.log.Info, __file__, "go search: " + t)
        if self.actions != None:
            if "searchAction" in self.actions:
                self.actions["searchAction"](t)
    
    def returnPressedAtSearch(self, event):
        '''Is called when user hits Return key while writing in search field'''
        t = self.entrySearchText.get()
        self.log.add(self.log.Info, __file__, "return search: " + t)
        
        if self.actions != None:
            if "searchAction" in self.actions:
                self.actions["searchAction"](t)
    
    def buttonNewClicked(self):
        self.log.add(self.log.Info, __file__, "new clicked")
        if self.actions != None:
            if "newAction" in self.actions:
                self.actions["newAction"]()
                