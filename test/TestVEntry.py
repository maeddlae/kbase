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


class TestVEntry(unittest.TestCase):


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

        self.entry = ModelEntry(self.log, "animals")
        self.entry.description = "these are animals"
        self.entry.keywords.append("deer")
        self.entry.keywords.append("bear")

    def tearDown(self):
        pass
    
    def dummy1(self, newName):
        pass
    
    def dummy2(self):
        pass
    
    def dummy3(self):
        pass

    def testDrawEntry(self):
        '''Tests whether all elements of the entry are drawn'''
        self.ventry.drawEntry(self.entry)
        self.ventry.update()
        
        exp = "animals"
        act = self.ventry.name.get("1.0", 'end-1c')
        self.assertEqual(exp, act)
        
        exp = "these are animals"
        act = self.ventry.description.get("1.0", 'end-1c')
        self.assertEqual(exp, act)
        
        exp = "deer bear"
        act = self.ventry.keywords.get("1.0", 'end-1c')
        
    def testReturnPressedAtName(self):
        '''Tests whether the right method is called at Return keypress on name'''
        self.ventry.drawEntry(self.entry)
        self.ventry.grid()
        self.root.update()
        self.ventry.name.delete("1.0", END)
        self.ventry.name.insert(END, "new name")
        self.ventry.name.focus_force()
        self.ventry.name.event_generate("<Return>")
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