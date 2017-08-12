'''
Created on 24 Jul 2017

@author: Mathias Bucher
'''

from Tkinter import *
from VEntry import VEntry
from VSearch import VSearch

class View(object):
    '''
    This class holds the entire GUI of the application
    '''


    def __init__(self, log, buttonGoAction):
        '''Constructor: Creates the window'''
        self.log = log
        self.buttonGoAction = buttonGoAction
        
        self.root = Tk()
        self.root.title("kbase")
        self.root.geometry("400x500")
        
        self.app = Frame(self.root)
        self.entryView = VEntry(self.root, self.log)
        self.searchView = VSearch(self.root, self.log)
        self.app.grid()
        
        self.log.add(self.log.Info, __file__, "init" )
        
    def draw(self,entry):
        '''Draws the window with menu bar and entry'''
        self.drawMenuBar()
        self.entryView.drawEntry(entry)#todo remove
        self.root.mainloop()
        
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
        self.buttonGoAction(self.entrySearchText.get())
    