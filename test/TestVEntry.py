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
        
        self.actionlist = {"entryChangeAction" : self.dummy1,
                  "newImageAction" : self.dummy4}
        
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
        self.entry.keywords.append("deer")
        self.entry.keywords.append("bear")
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

    def testDrawEntryIfHasNoKeywords(self):
        '''Tests whether all elements of the entry are drawn'''
        self.entry.keywords = []
        
        self.ventry.drawEntry(self.entry)
        self.ventry.grid(sticky=W)
        self.root.update()
        
        exp = "animals"
        act = self.ventry.nameText.get("1.0", 'end-1c')
        self.assertEqual(exp, act)
        
        exp = "these are animals"
        act = self.ventry.description.get("1.0", 'end-1c')
        self.assertEqual(exp, act)
        
        self.assertEqual(1, self.ventry.keywords.children.__len__())
        exp = self.ventry.keywordPrompt
        act = self.ventry.keywords.winfo_children()[0]["text"]
        self.assertEqual(exp, act)
        
        self.assertEqual(1, self.ventry.images.children.__len__())
        
        self.assertEqual(2, self.ventry.files.children.__len__())

    def testDrawEntryIfHasKeywords(self):
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
        
        self.assertEqual(2, self.ventry.keywords.children.__len__())
        for exp, act in zip(self.entry.keywords, self.ventry.keywords.winfo_children()):
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
        self.ventry.showRightClickMenu = MagicMock()
        self.ventry.drawEntry(self.entry)
        self.ventry.grid()
        self.root.update()
        images = self.ventry.images.winfo_children()
        xpos = images[0].winfo_x()
        ypos = images[0].winfo_y()
        images[0].event_generate("<Button-3>", x=xpos+1, y=ypos+1)
        self.ventry.showRightClickMenu.assert_called_once()
        
    def testRightClickOnKeyword(self):
        '''Tests if right click menu would be drawn at right click'''
        self.ventry.showKeywordRightClickMenu = MagicMock()
        self.ventry.drawEntry(self.entry)
        self.ventry.grid()
        self.root.update()
        keywords = self.ventry.keywords.winfo_children()
        xpos = keywords[0].winfo_x()
        ypos = keywords[0].winfo_y()
        keywords[0].event_generate("<Button-3>", x=xpos+1, y=ypos+1)
        self.ventry.showKeywordRightClickMenu.assert_called_once()
        
    def testNewImageClick(self):
        '''Tests if new image is clicked correctly'''
        #todo
        pass
        
    def testDeleteImageClick(self):
        '''Tests if delete image is clicked correctly'''
        #todo
        pass
        
    def testNewKeywordClick(self):
        '''Tests if new keyword is clicked correctly'''
        #todo
        pass
        
    def testDeleteKeywordClick(self):
        '''Tests if delete keyword is clicked correctly'''
        #todo
        pass
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()