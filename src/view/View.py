'''
Created on 24 Jul 2017

@author: Mathias Bucher
'''

from Tkinter import *
from VEntry import VEntry
from VSearch import VSearch

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
        
        self.app = Frame(self.root)
        self.entryView = VEntry(self.root, self.log, self.actions)
        self.searchView = VSearch(self.root, self.log)
        self.app.grid()
        self.drawMenuBar()
        
        self.log.add(self.log.Info, __file__, "init" )
        
    def run(self):
        '''Calls Tkinter mainloop, which never returns!'''
        self.root.mainloop() # this is an infinite loop!
        
    def drawEntry(self, entry):
        self.searchView.grid_forget()
        self.entryView.drawEntry(entry)#todo remove
        self.entryView.grid(sticky=W)
        pass
    
    def drawSearch(self):
        # todo
        self.entryView.grid_forget()
        pass
        
    def drawMenuBar(self):
        '''Draws the menu bar at the top of the window'''
        self.entrySearchText = StringVar()
        self.entrySearch = Entry(self.app)
        self.entrySearch["textvariable"] = self.entrySearchText
        self.entrySearchText.set("...")
        self.entrySearch.grid(row=0, column=0, sticky=W)
        
        self.buttonGo = Button(self.app)
        self.buttonGo.grid(row=0, column=1, sticky=W)
        self.buttonGo["text"] = "go"
        self.buttonGo["command"] = self.buttonGo_click
    
    def buttonGo_click(self):
        self.log.add(self.log.Info, __file__, "button go clicked" )
        if self.actions != None:
            if "menuGoClicked" in self.actions:
                self.actions["menuGoClicked"](self.entrySearchText.get())
    