'''
Created on 14 Aug 2017

@author: Mathias Bucher
'''
import unittest
from Tkinter import *
from view.VEntry import VEntry
from ctr.Log import Log
from mock import MagicMock
from model.ModelEntry import ModelEntry
import os


class TestVEntry(unittest.TestCase):
    testImagePath = "testimage.jpg"
    testWordPath = "testword.docx"


    def setUp(self):
        self.log = Log("testlog.txt")
        self.log.add = MagicMock()
            
        self.root = Tk()
        self.root.title("kbase test")
        self.root.geometry("400x500")
        
        self.dummy1 = MagicMock()
        self.dummy4 = MagicMock()
        self.dummy5 = MagicMock()
        self.dummy6 = MagicMock()
        self.dummy7 = MagicMock()
        
        self.actionlist = {"entryChangeAction" : self.dummy1,
                  "newImageAction" : self.dummy4,
                  "addTagAction" : self.dummy5,
                  "deleteImageAction" : self.dummy6,
                  "deleteTagAction" : self.dummy7}
        
        self.ventry = VEntry(self.root, self.log, self.actionlist)

        
        if not os.path.exists(self.testImagePath):
            self.testImagePath = "../../test/" + self.testImagePath
            self.testWordPath = "../../test/" + self.testWordPath
        
        f = open(self.testImagePath, "rb")
        self.testImageStream = f.read()
        f.close()
        
        f = open(self.testWordPath, "rb")
        self.testWordStream = f.read()
        f.close()
        self.entry = ModelEntry(self.log, "animals")
        self.entry.description = "these are animals"
        self.entry.tags.append("deer")
        self.entry.tags.append("bear")
        self.entry.images.append(self.testImageStream)
        self.entry.files.append(self.testWordStream)
        self.entry.files.append(self.testImageStream)
        
    def tearDown(self):
        self.ventry.grid()
        self.root.update()
        self.root.destroy()
    
    def testGetName(self):
        '''Tests whether method returns right name'''
        self.ventry.drawEntry(self.entry)
        self.ventry.update()
        exp = self.entry.name
        act = self.ventry.getName()
        self.assertEqual(exp, act)

    def testDrawEntryIfHasNoTags(self):
        '''Tests whether all elements of the entry are drawn'''
        self.entry.tags = []
        
        self.ventry.drawEntry(self.entry)
        self.ventry.grid(sticky=W)
        self.root.update()
        
        exp = "animals"
        act = self.ventry.nameText.get("1.0", 'end-1c')
        self.assertEqual(exp, act)
        
        exp = "these are animals"
        act = self.ventry.description.get("1.0", 'end-1c')
        self.assertEqual(exp, act)
        
        self.assertEqual(1, self.ventry.tags.children.__len__())
        exp = self.ventry.tagPrompt
        act = self.ventry.tags.winfo_children()[0]["text"]
        self.assertEqual(exp, act)
        
        self.assertEqual(1, self.ventry.images.children.__len__())
        
        self.assertEqual(2, self.ventry.files.children.__len__())

    def testDrawEntryIfHasNoImages(self):
        '''Tests whether all elements of the entry are drawn'''
        self.entry.images = []
        
        self.ventry.drawEntry(self.entry)
        self.ventry.grid(sticky=W)
        self.root.update()
        
        exp = "animals"
        act = self.ventry.nameText.get("1.0", 'end-1c')
        self.assertEqual(exp, act)
        
        exp = "these are animals"
        act = self.ventry.description.get("1.0", 'end-1c')
        self.assertEqual(exp, act)
        
        self.assertEqual(2, self.ventry.tags.children.__len__())
        for exp, act in zip(self.entry.tags, self.ventry.tags.winfo_children()):
            self.assertEqual(exp, act["text"])
        
        self.assertEqual(1, self.ventry.images.children.__len__())
        exp = self.ventry.imagePrompt
        act = self.ventry.images.winfo_children()[0]["text"]
        self.assertEqual(exp, act)
        
        self.assertEqual(2, self.ventry.files.children.__len__())

    def testDrawEntry(self):
        '''Tests whether all elements of the entry are drawn'''
        self.ventry.drawEntry(self.entry)
        self.ventry.grid(sticky=W)
        self.root.update()
        
        exp = "animals"
        act = self.ventry.nameText.get("1.0", 'end-1c')
        self.assertEqual(exp, act)
        
        exp = "these are animals"
        act = self.ventry.description.get("1.0", 'end-1c')
        self.assertEqual(exp, act)
        
        self.assertEqual(2, self.ventry.tags.children.__len__())
        for exp, act in zip(self.entry.tags, self.ventry.tags.winfo_children()):
            self.assertEqual(exp, act["text"])
        
        self.assertEqual(1, self.ventry.images.children.__len__())
        
        self.assertEqual(2, self.ventry.files.children.__len__())
        
    def testReturnPressedAtFields(self):
        '''Tests whether the right method is called at Return keypress'''
        self.ventry.drawEntry(self.entry)
        self.ventry.grid()
        self.root.update()
        self.ventry.nameText.delete("1.0", END)
        self.ventry.nameText.insert(END, "new name")
        self.ventry.description.delete("1.0", END)
        self.ventry.description.insert(END, "new description")
        self.ventry.nameText.focus_force()
        self.ventry.nameText.event_generate("<Return>")
        self.dummy1.assert_called_once_with("new name", "new description")
        
        self.ventry.nameText.delete("1.0", END)
        self.ventry.nameText.insert(END, "new name")
        self.ventry.description.delete("1.0", END)
        self.ventry.description.insert(END, "new description")
        self.dummy1.reset_mock()
        self.ventry.description.focus_force()
        self.ventry.description.event_generate("<Return>")
        self.dummy1.assert_called_once_with("new name", "new description")
        
    def testRightClickOnImage(self):
        '''Tests if right click menu would be drawn at right click'''
        self.ventry.showImageRightClickMenu = MagicMock()
        self.ventry.drawEntry(self.entry)
        self.ventry.grid()
        self.root.update()
        images = self.ventry.images.winfo_children()
        xpos = images[0].winfo_x()
        ypos = images[0].winfo_y()
        images[0].event_generate("<Button-3>", x=xpos+1, y=ypos+1)
        self.ventry.showImageRightClickMenu.assert_called_once()
        
    def testRightClickOnTag(self):
        '''Tests if right click menu would be drawn at right click'''
        self.ventry.showTagRightClickMenu = MagicMock()
        self.ventry.drawEntry(self.entry)
        self.ventry.grid()
        self.root.update()
        tags = self.ventry.tags.winfo_children()
        xpos = tags[0].winfo_x()
        ypos = tags[0].winfo_y()
        tags[0].event_generate("<Button-3>", x=xpos+1, y=ypos+1)
        self.ventry.showTagRightClickMenu.assert_called_once()
        
    def testNewTagClicked(self):
        '''Checks what happens if new tag is called. This test does 
        not include the calling mechanism of newTagClicked method 
        itself. It tests the return pressed action instead'''
        self.entry.tags = []
        self.ventry.drawEntry(self.entry)
        self.ventry.grid()
        self.root.update()
        
        # check if tag prompt is shown
        self.assertEqual(1, self.ventry.tags.children.__len__())
        exp = self.ventry.tagPrompt
        act = self.ventry.tags.winfo_children()[0]["text"]
        self.assertEqual(exp, act)
        self.root.update()
        
        self.ventry.newTagClicked()
        self.root.update()
        
        # test if enter tag prompt appears
        self.assertEqual(1, self.ventry.tags.children.__len__())
        exp = self.ventry.tagEnterPrompt
        act = self.ventry.tags.winfo_children()[0].get("1.0", 'end-1c')
        self.assertEqual(exp, act)
        
        # user enters now tag
        newTag = "adsfae"
        self.ventry.newTagText.delete("1.0", END)
        self.ventry.newTagText.insert(END, newTag)
        self.dummy5.reset_mock()
        self.ventry.newTagText.focus_force()
        self.ventry.newTagText.event_generate("<Return>")
        self.dummy5.assert_called_once_with(newTag)
        
        
    def testNewImageClick(self):
        '''Tests if new image is clicked correctly'''
        #todo
        pass
        
    def testDeleteImageClickedWithImage(self):
        '''Tests if delete image works. This test does not include the 
        event calling of the widget, it tests the content of 
        deleteImageClicked method only'''
        self.ventry.drawEntry(self.entry)
        self.ventry.grid()
        self.root.update()
        self.ventry.clickedImage = self.ventry.images.winfo_children()[0]
        self.ventry.deleteImageClicked()
        self.dummy6.assert_called_once_with(0)
        
    def testDeleteImageClickedWithoutImage(self):
        '''Tests if delete image works. This test does not include the 
        event calling of the widget, it tests the content of 
        deleteImageClicked method only'''
        self.entry.images = []
        self.ventry.drawEntry(self.entry)
        self.ventry.grid()
        self.root.update()
        self.ventry.clickedImage = self.ventry.images.winfo_children()[0]
        self.ventry.deleteImageClicked()
        self.dummy6.assert_not_called()
        
    def testNewTagClick(self):
        '''Tests if new tag is clicked correctly'''
        #todo
        pass
        
        
    def testDeleteTagClickedWithTag(self):
        '''Tests if delete tag works. This test does not include the 
        event calling of the widget, it tests the content of 
        deleteTagClicked method only'''
        self.ventry.drawEntry(self.entry)
        self.ventry.grid()
        self.root.update()
        self.ventry.clickedTag = self.ventry.tags.winfo_children()[1]
        expArg = self.ventry.clickedTag["text"]
        self.ventry.deleteTagClicked()
        self.dummy7.assert_called_once_with(expArg)
        
    def testDeleteTagClickedWithoutTag(self):
        '''Tests if delete tag works. This test does not include the 
        event calling of the widget, it tests the content of 
        deleteTagClicked method only'''
        self.entry.tags = []
        self.ventry.drawEntry(self.entry)
        self.ventry.grid()
        self.root.update()
        self.ventry.clickedTag = self.ventry.tags.winfo_children()[0]
        self.ventry.deleteTagClicked()
        self.dummy7.assert_not_called()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()