'''
Created on 24 Jul 2017

@author: Mathias Bucher
'''

from Tkinter import *

class View(Frame):
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
        self.clearEntry()
        
        if entry==None:
            self.labelNothingFound = Label(self.app)
            self.labelNothingFound["text"] = "nothing found"
            self.labelNothingFound.grid(row=1, column=0, columnspan=3, sticky=W)
        else:            
            self.labelName = Label(self.app)
            self.labelName["text"] = entry.name
            self.labelName.grid(row=1, column=0, columnspan=3, sticky=W)
            
            self.labelDescription = Label(self.app)
            self.labelDescription["text"] = entry.description
            self.labelDescription.grid(row=2, column=0, columnspan=3, sticky=W)
            
            self.labelKeywords = Label(self.app)
            self.labelKeywords["text"] = self.getKeywordString(entry.keywords)
            self.labelKeywords.grid(row=3, column=0, columnspan=3, sticky=W)
            
    def getKeywordString(self, keywords):
        s = ""
        for k in keywords:
            s += k + " "
        return s
    
    def clearEntry(self):
        if hasattr(self, 'labelNothingFound'):
            self.labelNothingFound.grid_forget()
        if hasattr(self, 'labelName'):
            self.labelName.grid_forget()
        if hasattr(self, 'labelText'):
            self.labelText.grid_forget()
        if hasattr(self, 'labelKeywords'):
            self.labelKeywords.grid_forget()
    
    def buttonGo_click(self):
        # todo: connect to action listener here
        self.log.add(self.log.Info, __file__, "button go clicked" )
        self.buttonGoAction(self.entrySearchText.get())
    
    def buttonEdit_click(self):
        # todo: connect to action listener here
        self.log.add(self.log.Info, __file__, "button edit clicked" )
        