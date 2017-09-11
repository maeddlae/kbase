'''
Created on 12 Aug 2017

@author: Mathias Bucher
'''
from Tkinter import Frame
from VStyles import rootColor, getLabel, getFrame, getButtonEntry

class VSearch(Frame):
    '''
    Shows search results
    '''

    def __init__(self, parent, log, actions):
        '''
        Constructor
        '''
        Frame.__init__(self, parent)
        self.configure(bg=rootColor)
        self.log = log
        self.actions = actions
        self.buttonName = []
        self.buttonTag = []
        self.buttonDescription = []
        self.log.add(self.log.Info, __file__, "init" )
        
    def removeOldResults(self):
        '''Removes the old results'''
        self.labelName.destroy()
        self.frameName.destroy()
        self.labelTag.destroy()
        self.frameTag.destroy()
        self.labelDescription.destroy()
        self.frameDescription.destroy()
        
        self.buttonName = []
        self.buttonTag = []
        self.buttonDescription = []
        
    def drawSearchResults(self, results):
        '''Draws the found search results sorted by name, tag and 
        description match'''
        self.labelName = getLabel(self, "found by name:")
        self.labelName.grid(row=0)
        
        self.frameName = getFrame(self)
        for i, e in enumerate(results["name"]):
            but = getButtonEntry(self.frameName, command=lambda n=e.name: self.buttonEntryClicked(n))
            self.buttonName.append(but)
            self.buttonName[i].grid(row=1, column=i)
            self.buttonName[i]["text"] = e.name
        self.frameName.grid()
        
        self.labelTag = getLabel(self, "found by tag:")
        self.labelTag.grid(row=2)
        
        self.frameTag = getFrame(self)
        for i, e in enumerate(results["tag"]):
            but = getButtonEntry(self.frameTag, command=lambda n=e.name: self.buttonEntryClicked(n))
            self.buttonTag.append(but)
            self.buttonTag[i].grid(row=3, column=i)
            self.buttonTag[i]["text"] = e.name
        self.frameTag.grid()
        
        self.labelDescription = getLabel(self, "found by description:")
        self.labelDescription.grid(row=4)
        
        self.frameDescription = getFrame(self)
        for i, e in enumerate(results["description"]):
            but = getButtonEntry(self.frameDescription, command=lambda n=e.name: self.buttonEntryClicked(n))
            self.buttonDescription.append(but)            
            self.buttonDescription[i].grid(row=5, column=i)
            self.buttonDescription[i]["text"] = e.name
        self.frameDescription.grid()
            
    def buttonEntryClicked(self, entryName):
        '''This method is called when any showed entry is clicked'''
        self.log.add(self.log.Info, __file__, entryName + " clicked")
        
        if self.actions != None:
            if "showEntryAction" in self.actions:
                self.actions["showEntryAction"](entryName)