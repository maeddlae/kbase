'''
Created on 14 Aug 2017

@author: Mathias Bucher
'''
import unittest
from mock import MagicMock
from ctr.Controller import Controller
from ctr.Log import Log
from model.Model import Model
from view.View import View
from model.ModelEntry import ModelEntry


class TestController(unittest.TestCase):


    def setUp(self):
        self.log = Log("testlog.txt")
        self.log.add = MagicMock()
        Log.add = MagicMock()        
        self.ctr = Controller()
        self.ctr.currentEntry = ModelEntry(self.log, "furniture")
        self.ctr.currentEntry.description = "This is the description of furniture"
        self.ctr.currentEntry.keywords.append("chair")
        self.ctr.currentEntry.keywords.append("table")

    def tearDown(self):
        pass

    def testEntryNameChangeAction(self):
        '''Checks if the right method of model is called'''
        self.ctr.model.updateNameOfEntry = MagicMock()
        self.ctr.entryNameChangeAction("roofs")
        self.ctr.model.updateNameOfEntry.assert_called_with(self.ctr.currentEntry, "roofs")
        self.assertEqual("roofs", self.ctr.currentEntry.name)
    
    def testEntryDescriptionChangeAction(self):
        '''Checks if the right method of model is called'''
        self.ctr.model.updateContentOfEntry= MagicMock()
        self.ctr.entryDescriptionChangeAction("new description")
        self.ctr.model.updateContentOfEntry.assert_called_with(self.ctr.currentEntry)
        self.assertEqual("new description", self.ctr.currentEntry.description)

    def testEntryKeywordChangeAction(self):
        '''Checks if the right method of model is called'''
        self.ctr.model.updateContentOfEntry= MagicMock()
        self.ctr.entryKeywordChangeAction("window")
        self.ctr.model.updateContentOfEntry.assert_called_with(self.ctr.currentEntry)
        s = self.ctr.currentEntry.getStringFromKeywords(self.ctr.currentEntry.keywords)
        self.assertEqual("window", s)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testads']
    unittest.main()