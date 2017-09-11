'''
Created on 24 Jul 2017

@author: Mathias Bucher
'''

from Tkinter import W
import tkFileDialog
from VMenubar import VMenubar
from VTab import VTab
from VDbPath import VDbPath
from VStyles import getRoot

class View():
    '''
    This class holds the entire GUI of the application
    '''


    def __init__(self, log, dbPath, actions):
        '''Constructor: Creates the window'''
        self.log = log
        self.actions = actions
        
        
        self.root = getRoot()
        
        self.dbPath = VDbPath(self.root, self.log, self.actions)
        self.dbPath.draw(dbPath)
        self.dbPath.grid(sticky=W)
        
        self.menubar = VMenubar(self.root, self.log, self.actions)
        self.menubar.draw()
        self.menubar.grid(sticky=W)
        
        self.tabs = VTab(parent=self.root, log=self.log, actions=self.actions)
        
        self.log.add(self.log.Info, __file__, "init" )
        
    def run(self):
        '''Calls Tkinter mainloop, which never returns!'''
        self.root.mainloop() # this is an infinite loop!
        
    def drawEntry(self, entry):
        self.menubar.enableButtonClose()
        self.menubar.enableButtonDelete()
        self.tabs.addEntry(entry)
        self.tabs.grid(sticky=W)
    
    def drawSearch(self, results):
        self.menubar.enableButtonClose()
        self.tabs.setSearch(results)
        self.tabs.grid(sticky=W)
        
    def removeEntry(self, entry):
        self.tabs.removeEntry(entry)
        if not self.tabs.hasTabs():
            self.menubar.disableButtonClose()    
            self.menubar.disableButtonDelete()    

    def removeSearch(self):
        self.tabs.removeSearch()
        if not self.tabs.hasTabs():
            self.menubar.disableButtonClose()
            
    def setDeleteButton(self, on):
        '''Sets the state of the delete button. On = True = clickable'''
        if on == True:
            self.menubar.enableButtonDelete()
        else:
            self.menubar.disableButtonDelete()
            
    def changeDbPath(self, newPath):
        self.dbPath.changePath(newPath)
        
    def showNewImageSelectDialog(self):
        '''Shows a file dialog where user can select the 
        image to load'''
        filename = tkFileDialog.askopenfilename()
        
        if self.actions != None:
            if "imageSelectedAction" in self.actions:
                self.actions["imageSelectedAction"](filename)
        
    def showNewFileSelectDialog(self):
        '''Shows a file dialog where user can select the 
        file to load'''
        filename = tkFileDialog.askopenfilename()
        
        if self.actions != None:
            if "fileSelectedAction" in self.actions:
                self.actions["fileSelectedAction"](filename)
        