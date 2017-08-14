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
        
        self.ventry = VEntry(self.root, self.log, None)

        self.entry = ModelEntry(self.log, "animals")
        self.entry.description = "these are animals"
        self.entry.keywords.append("deer")
        self.entry.keywords.append("bear")

    def tearDown(self):
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
        #self.assertEqual(exp, act)
        
       # self.ventry.labelN
        
       # self.assertEqual(self.entry.name, self.ventry.labelName, msg)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()