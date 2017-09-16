'''
Created on 25 Aug 2017

@author: Mathias Bucher
'''
from Tkinter import Frame, StringVar
from VStyles import rootColor, getEntrySmall, getLabelSmall

class VDbPath(Frame):
    '''
    classdocs
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
        
    def draw(self, dbPath):
        '''Draws the database path widget'''
        self.dbLabel = getLabelSmall(self, "Database:")
        self.dbLabel.grid(row=0, column=0)
        
        self.dbPathEntryText = StringVar()
        self.dbPathEntry = getEntrySmall(self)
        self.dbPathEntry["textvariable"] = self.dbPathEntryText
        self.dbPathEntryText.set(dbPath)
        self.dbPathEntry.grid(row=0, column=1)
        self.dbPathEntry.bind( "<Return>", self.returnPressedAtPath)
        
    def changePath(self, newDbPath):
        '''Changes the displayed database path'''
        self.dbPathEntryText.set(newDbPath)
        
    def returnPressedAtPath(self, _event):
        '''Is called when user hits return while in 
        path field'''
        t = self.dbPathEntryText.get()
        self.log.add(self.log.Info, __file__, "return path: " + t)
        
        if self.actions != None:
            if "pathChangeAction" in self.actions:
                self.actions["pathChangeAction"](t)