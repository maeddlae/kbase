'''
Created on 24 Jul 2017

@author: Mathias Bucher
'''

from Tkinter import *
from VEntry import VEntry
from VSearch import VSearch
from VMenubar import VMenubar

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
        self.entryView = VEntry(self.root, self.log, self.actions)
        self.searchView = VSearch(self.root, self.log, self.actions)
        
        self.menubar.draw()
        self.menubar.grid(sticky=W)
        
        self.log.add(self.log.Info, __file__, "init" )
        
    def run(self):
        '''Calls Tkinter mainloop, which never returns!'''
        self.root.mainloop() # this is an infinite loop!
        
    def drawEntry(self, entry):
        self.searchView.grid_forget()
        self.entryView.drawEntry(entry)#todo remove
        self.entryView.grid(sticky=W)
    
    def drawSearch(self, results):
        # todo
        self.entryView.grid_forget()
        self.searchView.drawSearchResults(results)
        self.searchView.grid(sticky=W)
