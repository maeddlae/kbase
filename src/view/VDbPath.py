'''
Created on 25 Aug 2017

@author: Mathias Bucher
'''
from Tkinter import Frame, StringVar
from VStyles import rootColor, getEntry

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
        self.dbPathEntryText = StringVar()
        self.dbPathEntry = getEntry(self)
        self.dbPathEntry["textvariable"] = self.dbPathEntryText
        self.dbPathEntryText.set(dbPath)
        self.dbPathEntry.grid()
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