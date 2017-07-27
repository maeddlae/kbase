'''
Created on 24 Jul 2017

@author: Mathias Bucher
'''

from ctr.Log import Log
from Tkinter import *

class View(Frame):
    '''
    classdocs
    '''


    def __init__(self, log):
        '''Constructor: Creates the window'''
        self.log = log
        
        self.root = Tk()
        self.root.title("kbase")
        self.root.geometry("400x500")
        
        self.app = Frame(self.root)
        self.app.grid()
        
        self.log.add(self.log.Info, __file__, "init" )
        
    def draw(self,entry):
        '''Draws the window with menu bar and entry'''
        self.drawMenuBar()
        self.drawEntry(entry)
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
        
        self.buttonEdit = Button(self.app)
        self.buttonEdit.grid(row=0, column=2, sticky=W)
        self.buttonEdit["text"] = "edit"
        self.buttonEdit["command"] = self.buttonEdit_click
        
    def drawEntry(self,entry):
        '''Draws an entry. If the entry is None, it prints "nothing found"'''
        if entry==None:
            title = "nothing found"
        else:
            title = "todo enter title"
            
        self.labelTitle = Label(self.app)
        self.labelTitle["text"] = title
        self.labelTitle.grid(row=1, column=0, columnspan=3, sticky=W)
        
        self.labelText = Label(self.app)
        self.labelText["text"] = "this is the text"
        self.labelText.grid(row=2, column=0, columnspan=3, sticky=W)
        
        self.labelKeywords = Label(self.app)
        self.labelKeywords["text"] = "these are the keywords"
        self.labelKeywords.grid(row=3, column=0, columnspan=3, sticky=W)
    
    def buttonGo_click(self):
        # todo: connect to action listener here
        self.log.add(self.log.Info, __file__, "button go clicked" )
        pass
    
    def buttonEdit_click(self):
        # todo: connect to action listener here
        self.log.add(self.log.Info, __file__, "button edit clicked" )
        pass
        