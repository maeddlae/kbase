'''
Created on 24 Jul 2017

@author: Mathias Bucher
'''

from Tkinter import *
from VMenubar import VMenubar
from VTab import VTab

class View():
    '''
    This class holds the entire GUI of the application
    '''


    def __init__(self, log, actions):
        '''Constructor: Creates the window'''
        self.log = log
        self.actions = actions
        
        self.root = Tk()
        self.root.title("kbase")
        self.root.geometry("400x500")
        
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