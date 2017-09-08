'''
Created on 12 Aug 2017

@author: Mathias Bucher
'''
from Tkinter import Frame
from Tkinter import Menu
from Tkinter import Label
from Tkinter import Button
from Tkinter import Text
from Tkinter import END, W
from Tkinter import Scrollbar
from PIL import Image, ImageTk
import io
from mock.mock import right

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
            self.nameText.bind( "<Return>", self.returnPressedInTextFields)
            
            self.description = Text(self, height=6, width=self.width10, font=("Helvetica", 10))
            self.description.insert(END, entry.description)
            self.description.grid(row=1, column=0, sticky=W)
            self.description.bind( "<Return>", self.returnPressedInTextFields)
            
            descScrollbar = Scrollbar(self, command=self.description.yview)
            descScrollbar.grid(row=1, column=1, sticky=W)
            self.description['yscrollcommand'] = descScrollbar.set            
            
            self.keywords = Frame(self)
            for i, key in enumerate(entry.keywords):
                keyLabel = Label(self.keywords, text=key)
                keyLabel.grid(row=2, column=i, sticky=W)
                keyLabel.bind("<Button-3>", self.showRightClickMenu)
            self.keywords.grid(sticky=W)
            
            self.rightClickMenu = Menu(self, tearoff=0)
            self.rightClickMenu.add_command(label="new", 
                                       command=self.newImageClicked)
            self.rightClickMenu.add_command(label="delete", 
                                       command=self.deleteImageClicked)
            
            self.images = Frame(self)
            for i, img in enumerate(entry.images):
                iobytes = io.BytesIO(img)
                img = Image.open(iobytes)
                img.thumbnail(self.imageSize, Image.ANTIALIAS )
                photoimg = ImageTk.PhotoImage(img)
                imgLabel = Label(self.images, image=photoimg)
                imgLabel.image = photoimg
                imgLabel.grid(row=3, column=i, sticky=W)
                imgLabel.bind("<Button-3>", self.showRightClickMenu)
            self.images.grid(sticky=W)
            
            self.files = Frame(self)
            for i, fil in enumerate(entry.files):
                lbl = Label(self.files)
                lbl["text"] = "file"
                lbl.grid(row=4, column=i, sticky=W)
            self.files.grid(sticky=W)
            
            self.log.add(self.log.Info, __file__, "entry " + entry.name + " drawn" )

    def showRightClickMenu(self, event):
        '''Tries to show the right click menu'''
        try:
            self.rightClickMenu.tk_popup(event.x_root, event.y_root+20, 0)
        finally:
            self.rightClickMenu.grab_release()

    def getName(self):
        '''Returns the name of the displayed entry'''
        return self.nameText.get("1.0", 'end-1c')

    def returnPressedInTextFields(self, event):
        '''Is called when user hits Return key while writing in name field'''
        name = self.nameText.get("1.0", 'end-1c')
        description = self.description.get("1.0", 'end-1c')
        self.log.add(self.log.Info, __file__, "name change: " + name)
        
        if self.actions != None:
            if "entryChangeAction" in self.actions:
                self.actions["entryChangeAction"](name, description)

    def deleteImageClicked(self):
        '''Is called when user right clicks on an image and selects delete'''
        self.log.add(self.log.Info, __file__, "delete image clicked" )
                
        if self.actions != None:
            if "deleteImageAction" in self.actions:
                self.actions["deleteImageAction"]()

    def newImageClicked(self):
        '''Is called when user right clicks on an image and selects new'''
        self.log.add(self.log.Info, __file__, "new image clicked" )
                
        if self.actions != None:
            if "newImageAction" in self.actions:
                self.actions["newImageAction"]()