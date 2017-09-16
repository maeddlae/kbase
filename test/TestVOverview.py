'''
Created on 16 Sep 2017

@author: Mathias Bucher
'''
import unittest
from Tkinter import *
from view.VOverview import VOverview
from ctr.Log import Log
from mock import MagicMock
from model.ModelEntry import ModelEntry
from collections import OrderedDict


class TestVOverview(unittest.TestCase):


    def setUp(self):
        self.log = Log("testlog.txt")
        self.log.add = MagicMock()
        
        self.root = Tk()
        self.root.title("kbase test")
        self.root.geometry("400x500")
        
        self.dummy = MagicMock()
        
        self.actionlist = {"showEntryOverviewAction" : self.dummy}
        
        self.voverview = VOverview(self.root, self.log, self.actionlist)

        self.e1 = ModelEntry(self.log, "e1")
        self.e2 = ModelEntry(self.log, "e2")
        self.e3 = ModelEntry(self.log, "k")
        self.e4 = ModelEntry(self.log, "z")

        self.entries = OrderedDict()
        self.entries["e"] = [self.e1, self.e2]
        self.entries["k"] = [self.e3]
        self.entries["z"] = [self.e4]

    def tearDown(self):
        self.voverview.grid()
        self.root.update()
        self.root.destroy()


    def testShow(self):
        self.voverview.show(self.entries)
        self.voverview.grid()
        self.voverview.update()
        
        self.assertEqual("e1", self.voverview.sortedEntries["e"].winfo_children()[0]["text"])
        self.assertEqual("e2", self.voverview.sortedEntries["e"].winfo_children()[1]["text"])
        self.assertEqual("k", self.voverview.sortedEntries["k"].winfo_children()[0]["text"])
        self.assertEqual("z", self.voverview.sortedEntries["z"].winfo_children()[0]["text"])

    def testClickEntry(self):
        self.voverview.show(self.entries)
        self.voverview.grid()
        self.voverview.update()
        
        self.voverview.sortedEntries["e"].winfo_children()[0].focus_force()
        self.voverview.sortedEntries["e"].winfo_children()[0].invoke()
        self.dummy.assert_called_with(self.e1.name)
        
        self.voverview.sortedEntries["k"].winfo_children()[0].focus_force()
        self.voverview.sortedEntries["k"].winfo_children()[0].invoke()
        self.dummy.assert_called_with(self.e3.name)
        
    def testRemoveAll(self):
        self.voverview.show(self.entries)
        self.voverview.grid()
        self.voverview.update()
        
        self.assertEqual(3, self.voverview.sortedEntries.items().__len__())
        
        self.voverview.removeAll()
        self.voverview.grid()
        self.voverview.update()
        
        self.assertEqual(0, self.voverview.sortedEntries.items().__len__())
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()