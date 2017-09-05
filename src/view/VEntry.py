'''
Created on 12 Aug 2017

@author: Mathias Bucher
'''
from Tkinter import Frame
from Tkinter import Label
from Tkinter import Button
from Tkinter import Text
from Tkinter import END, W
from Tkinter import Scrollbar
from PIL import Image, ImageTk
import io

class VEntry(Frame):
    '''
    Shows an entry and allows changes on it.
    '''
    width10=50
    width15=32
    imageSize=100,100

    def __init__(self, parent, log, actions):
        '''
        Constructor
        '''
        Frame.__init__(self, parent)
        self.log = log
        self.actions = actions
        self.log.add(self.log.Info, __file__, "init" )
            
    def drawEntry(self, entry):
        '''Draws an entry. If the entry is None, it does nothing'''
        if entry != None:
            self.nameText = Text(self, height=1, width=self.width15, font=("Helvetica", 15, "bold"))
            self.nameText.insert(END, entry.name)
            self.nameText.grid(row=0, column=0, sticky=W)
            self.nameText.bind( "<Return>", self.returnPressedAtName)
            
            self.description = Text(self, height=6, width=self.width10, font=("Helvetica", 10))
            self.description.insert(END, entry.description)
            self.description.grid(row=1, column=0, sticky=W)
            self.description.bind( "<Return>", self.returnPressedAtDescription)
            
            descScrollbar = Scrollbar(self, command=self.description.yview)
            descScrollbar.grid(row=1, column=1, sticky=W)
            self.description['yscrollcommand'] = descScrollbar.set
            
            self.keywords = Text(self, height=2, width=self.width10, font=("Helvetica", 10))
            s = entry.getStringFromKeywords(entry.keywords)
            self.keywords.insert(END, s)
            self.keywords.grid(row=2, sticky=W)
            self.keywords.bind( "<Return>", self.returnPressedAtKeywords)
            
            keyScrollbar = Scrollbar(self, command=self.keywords.yview)
            keyScrollbar.grid(row=2, column=1, sticky=W)
            self.keywords['yscrollcommand'] = keyScrollbar.set
            
            self.images = Frame(self)
            self.newImageButton = Button(self.images, command=self.buttonNewImageClicked)
            self.newImageButton["text"] = "new"
            self.newImageButton.grid(row=3, column=0, sticky=W)
            for i, img in enumerate(entry.images):
                iobytes = io.BytesIO(img)
                img = Image.open(iobytes)
                img.thumbnail(self.imageSize, Image.ANTIALIAS )
                photoimg = ImageTk.PhotoImage(img)
                imgLabel = Label(self.images, image=photoimg)
                imgLabel.image = photoimg
                imgLabel.grid(row=3, column=i+1, sticky=W)
            self.images.grid(sticky=W)
            
            self.files = Frame(self)
            for i, fil in enumerate(entry.files):
                lbl = Label(self.files)
                lbl["text"] = "file"
                lbl.grid(row=4, column=i, sticky=W)
            self.files.grid(sticky=W)
            
            self.log.add(self.log.Info, __file__, "entry " + entry.name + " drawn" )

    def getName(self):
        '''Returns the name of the displayed entry'''
        return self.nameText.get("1.0", 'end-1c')

    def returnPressedAtName(self, event):
        '''Is called when user hits Return key while writing in name field'''
        t = self.nameText.get("1.0", 'end-1c')
        self.log.add(self.log.Info, __file__, "name change: " + t)
        
        if self.actions != None:
            if "changeNameAction" in self.actions:
                self.actions["changeNameAction"](t)
        
    def returnPressedAtDescription(self, event):
        '''Is called when user hits Return key while writing in description field'''
        t = self.description.get("1.0", 'end-1c')
        self.log.add(self.log.Info, __file__, "description change: " + t)
                
        if self.actions != None:
            if "changeDescriptionAction" in self.actions:
                self.actions["changeDescriptionAction"](t)
    
    def returnPressedAtKeywords(self, event):
        '''Is called when user hits Return key while writing in keywords field'''
        t = self.keywords.get("1.0", 'end-1c')
        self.log.add(self.log.Info, __file__, "keywords change: " + t )
                
        if self.actions != None:
            if "changeKeywordsAction" in self.actions:
                self.actions["changeKeywordsAction"](t)

    def buttonNewImageClicked(self):
        '''Is called when user clicks new beside images'''
        self.log.add(self.log.Info, __file__, "new image clicked" )
                
        if self.actions != None:
            if "newImageAction" in self.actions:
                self.actions["newImageAction"]()