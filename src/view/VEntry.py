'''
Created on 12 Aug 2017

@author: Mathias Bucher
'''
from Tkinter import Frame
from Tkinter import Menu
from Tkinter import Label
from Tkinter import Text
from Tkinter import END, W
from Tkinter import Scrollbar
from PIL import Image, ImageTk
import io
from VStyles import rootColor, getLargeText, getSmallText, getScrollbar

class VEntry(Frame):
    '''
    Shows an entry and allows changes on it.
    '''
    width10=50
    width15=32
    imageSize=100,100
    tagPrompt = "right click here and add tags"
    tagEnterPrompt = "enter tag"
    imagePrompt = "right click here and add images"
    filePrompt = "right click here and add files"

    def __init__(self, parent, log, actions):
        '''
        Constructor
        '''
        Frame.__init__(self, parent)
        self.configure(bg=rootColor)
        self.log = log
        self.actions = actions
        self.log.add(self.log.Info, __file__, "init" )
            
    def drawEntry(self, entry):
        '''Draws an entry. If the entry is None, it does nothing'''
        if entry != None:
            self.nameText = getLargeText(self, entry.name)
            self.nameText.grid(row=0, column=0)
            self.nameText.bind( "<Return>", self.returnPressedInTextFields)
            
            self.description = getSmallText(self, entry.description)
            self.description.grid(row=1, column=0, sticky=W)
            self.description.bind( "<Return>", self.returnPressedInTextFields)
            
            descScrollbar = getScrollbar(self, self.description)
            descScrollbar.grid(row=1, column=1)   
            
            self.tagRightClickMenu = Menu(self, tearoff=0)
            self.tagRightClickMenu.add_command(label="new", 
                                       command=self.newTagClicked)
            self.tagRightClickMenu.add_command(label="delete", 
                                       command=self.deleteTagClicked)     
            
            self.tags = Frame(self)
            # if there are no tags, place label which prompts user to enter some
            if entry.tags.__len__() == 0:
                prompt = Label(self.tags, text=self.tagPrompt)
                prompt.grid(row=2, column=0, sticky=W)
                prompt.bind("<Button-3>", self.showTagRightClickMenu)
            else:
                for i, key in enumerate(entry.tags):
                    keyLabel = Label(self.tags, text=key)
                    keyLabel.grid(row=2, column=i, sticky=W)
                    keyLabel.bind("<Button-3>", self.showTagRightClickMenu)
            self.tags.grid(sticky=W)
            
            self.imageRightClickMenu = Menu(self, tearoff=0)
            self.imageRightClickMenu.add_command(label="new", 
                                       command=self.newImageClicked)
            self.imageRightClickMenu.add_command(label="delete", 
                                       command=self.deleteImageClicked)
            
            self.images = Frame(self)
            # if there are no images, place label which prompts user to enter some
            if entry.images.__len__() == 0:
                prompt = Label(self.images, text=self.imagePrompt)
                prompt.grid(row=3, column=0, sticky=W)
                prompt.bind("<Button-3>", self.showImageRightClickMenu)
            else:
                for i, img in enumerate(entry.images):
                    iobytes = io.BytesIO(img)
                    img = Image.open(iobytes)
                    img.thumbnail(self.imageSize, Image.ANTIALIAS )
                    photoimg = ImageTk.PhotoImage(img)
                    imgLabel = Label(self.images, image=photoimg)
                    imgLabel["text"] = str(i)
                    imgLabel.image = photoimg
                    imgLabel.grid(row=3, column=i, sticky=W)
                    imgLabel.bind("<Button-3>", self.showImageRightClickMenu)
            self.images.grid(sticky=W)
            
            self.fileRightClickMenu = Menu(self, tearoff=0)
            self.fileRightClickMenu.add_command(label="new", 
                                       command=self.newFileClicked)
            self.fileRightClickMenu.add_command(label="delete", 
                                       command=self.deleteFileClicked)
            
            self.files = Frame(self)
            # if there are no files, place label which prompts user to enter some
            if entry.files.__len__() == 0:
                prompt = Label(self.files, text=self.filePrompt)
                prompt.grid(row=4, column=0, sticky=W)
                prompt.bind("<Button-3>", self.showFilesRightClickMenu)
            else:
                for i, (key, _content) in enumerate(entry.files.iteritems()):
                    lbl = Label(self.files)
                    lbl["text"] = key
                    lbl.grid(row=4, column=i, sticky=W)
                    lbl.bind("<Button-3>", self.showFilesRightClickMenu)
            self.files.grid(sticky=W)
            
            self.log.add(self.log.Info, __file__, "entry " + entry.name + " drawn" )

    def returnPressedInTextFields(self, _event):
        '''Is called when user hits Return key while writing in name field'''
        name = self.nameText.get("1.0", 'end-1c')
        description = self.description.get("1.0", 'end-1c')
        self.log.add(self.log.Info, __file__, "name change: " + name)
        
        if self.actions != None:
            if "entryChangeAction" in self.actions:
                self.actions["entryChangeAction"](name, description)

    def getName(self):
        '''Returns the name of the displayed entry'''
        return self.nameText.get("1.0", 'end-1c')
            
    def showTagRightClickMenu(self, event):
        '''This menu appears if user right clicks on a tag'''
        try:
            self.clickedTag = event.widget
            self.tagRightClickMenu.tk_popup(event.x_root, event.y_root+20, 0)
        finally:
            self.tagRightClickMenu.grab_release()
                
    def newTagClicked(self):
        '''Is called when user right clicks on a tag and selects new'''
        self.log.add(self.log.Info, __file__, "new tag clicked" )
        
        # remove tag enter prompt
        if self.tags.winfo_children()[0]["text"] == self.tagPrompt:
            self.tags.winfo_children()[0].destroy()
                
        # add text widget for entering new tag
        self.newTagText = Text(self.tags, height=1, width=self.width15)
        self.newTagText.insert(END, self.tagEnterPrompt)
        self.newTagText.grid(row=3, column=0, sticky=W)
        self.newTagText.bind( "<Return>", self.returnPressedAtNewTag)
        self.tags.grid(sticky=W)
                
    def deleteTagClicked(self):
        '''Is called when user right clicks on a tag and selects new'''
        self.log.add(self.log.Info, __file__, "delete tag clicked" )
        
        # only call delete action if there is a tag
        if (self.tags.winfo_children().__len__() == 1 and 
            self.tags.winfo_children()[0]["text"] == self.tagPrompt):
            return
        else:
            tagToDelete = self.clickedTag["text"]
                    
            if self.actions != None:
                if "deleteTagAction" in self.actions:
                    self.actions["deleteTagAction"](tagToDelete)
                
    def returnPressedAtNewTag(self, _event):
        '''Is called when user hits Return key while adding a new tag'''
        newTag = self.newTagText.get("1.0", 'end-1c')
        self.log.add(self.log.Info, __file__, "new tag: " + newTag)
        
        if self.actions != None:
            if "addTagAction" in self.actions:
                self.actions["addTagAction"](newTag)

    def showImageRightClickMenu(self, event):
        '''Tries to show the right click menu'''
        try:
            self.clickedImage = event.widget
            self.imageRightClickMenu.tk_popup(event.x_root, event.y_root+20, 0)
        finally:
            self.imageRightClickMenu.grab_release()

    def deleteImageClicked(self):
        '''Is called when user right clicks on an image and selects delete'''
        self.log.add(self.log.Info, __file__, "delete image clicked" )
                
        # only call delete action if there is an image
        if (self.images.winfo_children().__len__() == 1 and 
            self.images.winfo_children()[0]["text"] == self.imagePrompt):
            return
        else:
            imageToDelete = int(self.clickedImage["text"])
            
            if self.actions != None:
                if "deleteImageAction" in self.actions:
                    self.actions["deleteImageAction"](imageToDelete)

    def newImageClicked(self):
        '''Is called when user right clicks on an image and selects new'''
        self.log.add(self.log.Info, __file__, "new image clicked" )
                
        # remove enter image prompt
        if self.images.winfo_children()[0]["text"] == self.imagePrompt:
            self.images.winfo_children()[0].destroy()
                
        if self.actions != None:
            if "newImageAction" in self.actions:
                self.actions["newImageAction"]()

    def showFilesRightClickMenu(self, event):
        '''Tries to show the right click menu'''
        try:
            self.clickedFile = event.widget
            self.fileRightClickMenu.tk_popup(event.x_root, event.y_root+20, 0)
        finally:
            self.fileRightClickMenu.grab_release()

    def deleteFileClicked(self):
        '''Is called when user right clicks on a file and selects delete'''
        self.log.add(self.log.Info, __file__, "delete file clicked" )
                
        # only call delete action if there is a file
        if (self.files.winfo_children().__len__() == 1 and 
            self.files.winfo_children()[0]["text"] == self.filePrompt):
            return
        else:
            fileToDelete = self.clickedFile["text"]
            
            if self.actions != None:
                if "deleteFileAction" in self.actions:
                    self.actions["deleteFileAction"](fileToDelete)

    def newFileClicked(self):
        '''Is called when user right clicks on a file and selects new'''
        self.log.add(self.log.Info, __file__, "new file clicked" )
                
        # remove enter file prompt
        if self.files.winfo_children()[0]["text"] == self.filePrompt:
            self.files.winfo_children()[0].destroy()
                
        if self.actions != None:
            if "newFileAction" in self.actions:
                self.actions["newFileAction"]()