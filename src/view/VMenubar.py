'''
Created on 17 Aug 2017

@author: Mathias Bucher
'''
from Tkinter import Frame, StringVar, DISABLED, NORMAL
from VStyles import rootColor, getButtonMenu, getEntry

class VMenubar(Frame):
    '''
    Draws and handles the menubar
    '''
    
    def __init__(self, parent, log, actions):
        '''
        Constructor
        '''
        Frame.__init__(self, parent)
        self.configure(bg=rootColor)
        self.log = log
        self.actions = actions
        self.log.add(self.log.Info, __file__, "init" )
        
    def draw(self):
        '''Draws the menu bar at the top of the window'''
        self.entrySearchText = StringVar()
        self.entrySearch = getEntry(self)
        self.entrySearch["textvariable"] = self.entrySearchText
        self.entrySearchText.set("search here")
        self.entrySearch.grid(row=0, column=0)
        self.entrySearch.bind( "<Return>", self.returnPressedAtSearch)
        
        self.buttonGo = getButtonMenu(self)
        self.buttonGo.grid(row=0, column=1)
        self.buttonGo["text"] = "go"
        self.buttonGo["command"] = self.buttonGoClicked
        
        self.buttonNew = getButtonMenu(self)
        self.buttonNew.grid(row=0, column=2)
        self.buttonNew["text"] = "new"
        self.buttonNew["command"] = self.buttonNewClicked
        
        self.buttonClose = getButtonMenu(self)
        self.buttonClose["state"] = DISABLED
        self.buttonClose.grid(row=0, column=3)
        self.buttonClose["text"] = "close"
        self.buttonClose["command"] = self.buttonCloseClicked
        
        self.buttonDelete = getButtonMenu(self)
        self.buttonDelete["state"] = DISABLED
        self.buttonDelete.grid(row=0, column=4)
        self.buttonDelete["text"] = "delete"
        self.buttonDelete["command"] = self.buttonDeleteClicked
        
        self.log.add(self.log.Info, __file__, "menu bar drawn" )
        
    def enableButtonClose(self):
        '''Makes close button clickable'''
        self.buttonClose["state"] = NORMAL
        self.buttonClose.grid()
        self.log.add(self.log.Info, __file__, "close button enabled")
        
    def disableButtonClose(self):
        '''Makes close button no more clickable'''
        self.buttonClose["state"] = DISABLED
        self.buttonClose.grid()
        self.log.add(self.log.Info, __file__, "close button disabled")
    
    def enableButtonDelete(self):
        '''Makes delete button clickable'''
        self.buttonDelete["state"] = NORMAL
        self.buttonDelete.grid()
        self.log.add(self.log.Info, __file__, "delete button enabled")
        
    def disableButtonDelete(self):
        '''Makes delete button no more clickable'''
        self.buttonDelete["state"] = DISABLED
        self.buttonDelete.grid()
        self.log.add(self.log.Info, __file__, "delete button disabled")
    
    def buttonGoClicked(self):
        t = self.entrySearchText.get()
        self.log.add(self.log.Info, __file__, "go search: " + t)
        if self.actions != None:
            if "searchAction" in self.actions:
                self.actions["searchAction"](t)
    
    def returnPressedAtSearch(self, _event):
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
    
    def buttonCloseClicked(self):
        self.log.add(self.log.Info, __file__, "close clicked")
        if self.actions != None:
            if "closedAction" in self.actions:
                self.actions["closedAction"]()
    
    def buttonDeleteClicked(self):
        self.log.add(self.log.Info, __file__, "delete clicked")
        if self.actions != None:
            if "deleteAction" in self.actions:
                self.actions["deleteAction"]()
                