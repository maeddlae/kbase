'''
Created on 19 Aug 2017

@author: Mathias Bucher
'''
import unittest
from Tkinter import *
from view.VTab import VTab
from view.VEntry import VEntry
from ctr.Log import Log
from mock import MagicMock
from model.ModelEntry import ModelEntry


class TestVTab(unittest.TestCase):


    def setUp(self):
        self.log = Log("testlog.txt")
        self.log.add = MagicMock()
        
        self.root = Tk()
        self.root.title("kbase test")
        self.root.geometry("400x500")
        
        self.vtab = VTab(parent=self.root, log=self.log, actions=None)

        self.results = {"name" : None}
        
        self.vtab.vsearch.drawSearchResults = MagicMock()
        self.vtab.vsearch.removeOldResults = MagicMock()
        
        self.entryDrawTemp = VEntry.drawEntry

    def tearDown(self):
        VEntry.drawEntry = self.entryDrawTemp

    def testSetSearchInitial(self):
        '''Tests whether initial search works'''        
        self.vtab.setSearch(self.results)
        # get all tab names. The names also include vtab's name 
        tabs = self.vtab.tabs()
        # gets the full name of vsearch widget
        vsearchName = "." + self.vtab._name + "." + self.vtab.vsearch._name
        # first tab should be 
        self.assertEqual(vsearchName, tabs[0])
        self.vtab.vsearch.drawSearchResults.assert_called_with(self.results)
        self.assertEqual(vsearchName, self.vtab.select(), "wrong tab is active")
    
    def testSetSearchASecondTime(self):
        '''Tests whether a second search overwrites the first one'''
        secondResults = { "Keyword" : None}
        self.vtab.setSearch(self.results)
        self.vtab.setSearch(secondResults)
        # get all tab names. The names also include vtab's name 
        tabs = self.vtab.tabs()
        # gets the full name of vsearch widget
        vsearchName = "." + self.vtab._name + "." + self.vtab.vsearch._name
        # first tab should be 
        self.assertEqual(vsearchName, tabs[0])
        self.vtab.vsearch.removeOldResults.assert_called()
        self.vtab.vsearch.drawSearchResults.assert_called_with(secondResults)
        self.assertEqual(vsearchName, self.vtab.select(), "wrong tab is active")
    
    def testAddEntry(self):
        '''Tests whether add works'''
        e = ModelEntry(self.log, "entry")
        self.vtab.addEntry(e)
        
        # get all tab names. The names also include vtab's name 
        tabs = self.vtab.tabs()
        # gets the full name of ventry widget
        ventryName = "." + self.vtab._name + "." + self.vtab.ventries[e.name]._name
        # first tab should be 
        self.assertEqual(ventryName, tabs[0])
        self.assertEqual(ventryName, self.vtab.select(), "wrong tab is active")
    
    def testAddExistingEntry(self):
        '''Trys to add an already existing entry'''
        e1 = ModelEntry(self.log, "e1")
        e2 = ModelEntry(self.log, "e2")
        self.vtab.addEntry(e1)
        self.vtab.addEntry(e2)
        self.vtab.addEntry(e1)
        self.assertEqual(2, self.vtab.tabs().__len__())
        self.assertEqual(2, self.vtab.ventries.__len__())
        
        # check if e1 is active tab
        ventryName = "." + self.vtab._name + "." + self.vtab.ventries[e1.name]._name
        self.assertEqual(ventryName, self.vtab.select(), "wrong tab is active")
    
    def testRemoveEntry(self):
        '''Removes an existing entry'''
        e = ModelEntry(self.log, "entry")
        self.vtab.addEntry(e)
        self.assertEqual(1, self.vtab.tabs().__len__())
        self.assertEqual(1, self.vtab.ventries.__len__())
        
        self.vtab.removeEntry(e)
        self.assertEqual(0, self.vtab.tabs().__len__())
        self.assertEqual(0, self.vtab.ventries.__len__())
    
    def testRemoveNotExistingEntry(self):
        '''Trys to remove a not existing entry'''
        e1 = ModelEntry(self.log, "e1")
        e2 = ModelEntry(self.log, "e2")
        self.vtab.addEntry(e1)
        self.vtab.addEntry(e2)
        self.assertEqual(2, self.vtab.tabs().__len__())
        self.assertEqual(2, self.vtab.ventries.__len__())
        
        self.vtab.removeEntry(e1)
        self.assertEqual(1, self.vtab.tabs().__len__())
        self.assertEqual(1, self.vtab.ventries.__len__())
        
        # get all tab names. The names also include vtab's name 
        tabs = self.vtab.tabs()
        # gets the full name of ventry widget
        ventryName = "." + self.vtab._name + "." + self.vtab.ventries[e2.name]._name
        # first tab should be 
        self.assertEqual(ventryName, tabs[0])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()