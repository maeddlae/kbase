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
        self.dummy2 = MagicMock()
        self.dummy3 = MagicMock()
        
        self.actionlist = {"changeNameAction" : self.dummy1,
                  "changeDescriptionAction" : self.dummy2,
                  "changeKeywordsAction" : self.dummy3}
        
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

    def testDrawEntry(self):
        '''Tests whether all elements of the entry are drawn'''
        self.ventry.drawEntry(self.entry)
        self.ventry.update()
        
        exp = "animals"
        act = self.ventry.nameText.get("1.0", 'end-1c')
        self.assertEqual(exp, act)
        
        exp = "these are animals"
        act = self.ventry.description.get("1.0", 'end-1c')
        self.assertEqual(exp, act)
        
        exp = "deer bear"
        act = self.ventry.keywords.get("1.0", 'end-1c')
        
        self.assertEqual(1, self.ventry.images.children.__len__())
        self.assertEqual(2, self.ventry.files.children.__len__())
        
    def testReturnPressedAtName(self):
        '''Tests whether the right method is called at Return keypress on name'''
        self.ventry.drawEntry(self.entry)
        self.ventry.grid()
        self.root.update()
        self.ventry.nameText.delete("1.0", END)
        self.ventry.nameText.insert(END, "new name")
        self.ventry.nameText.focus_force()
        self.ventry.nameText.event_generate("<Return>")
        self.dummy1.assert_called_with("new name")
    
    def testReturnPressedAtDescription(self):
        '''Tests whether the right method is called at Return keypress on description'''
        self.ventry.drawEntry(self.entry)
        self.ventry.grid()
        self.root.update()
        self.ventry.description.delete("1.0", END)
        self.ventry.description.insert(END, "new description")
        self.ventry.description.focus_force()
        self.ventry.description.event_generate("<Return>")
        self.dummy2.assert_called_with("new description")
    
    def testReturnPressedAtKeywords(self):
        '''Tests whether the right method is called at Return keypress on keywords'''
        self.ventry.drawEntry(self.entry)
        self.ventry.grid()
        self.root.update()
        self.ventry.keywords.delete("1.0", END)
        self.ventry.keywords.insert(END, "keyword")
        self.ventry.keywords.focus_force()
        self.ventry.keywords.event_generate("<Return>")
        self.dummy3.assert_called_with("keyword")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()