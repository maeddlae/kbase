'''
Created on 12 Aug 2017

@author: Mathias Bucher
'''
from Tkinter import *

class VEntry(Frame):
    '''
    Shows an entry and allows changes on it.
    '''

    def __init__(self, root, log):
        '''
        Constructor
        '''
        Frame.__init__(self, root)
        self.log = log
        self.log.add(self.log.Info, __file__, "init" )
        
            
    def drawEntry(self,entry):
        '''Draws an entry. If the entry is None, it prints "nothing found"'''
        self.clearEntry()
        
        if entry==None:
            self.labelNothingFound = Label(self)
            self.labelNothingFound["text"] = "nothing found"
            self.labelNothingFound.grid(row=1, column=0, columnspan=3, sticky=W)
        
        else:            
            self.labelName = Label(self)
            self.labelName["text"] = entry.name
            self.labelName.grid(row=1, column=0, columnspan=3, sticky=W)
            
            self.labelDescription = Label(self)
            self.labelDescription["text"] = entry.description
            self.labelDescription.grid(row=2, column=0, columnspan=3, sticky=W)
            
            self.labelKeywords = Label(self)
            self.labelKeywords["text"] = self.getKeywordString(entry.keywords)
            self.labelKeywords.grid(row=3, column=0, columnspan=3, sticky=W)
            
        self.grid()
        
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
        if hasattr(self, 'labelDescription'):
            self.labelDescription.grid_forget()
        if hasattr(self, 'labelKeywords'):
            self.labelKeywords.grid_forget()