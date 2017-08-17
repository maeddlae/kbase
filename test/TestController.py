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
        self.ctr = Controller( self.log )
        self.ctr.currentEntry = ModelEntry(self.log, "furniture")
        self.ctr.currentEntry.description = "This is the description of furniture"
        self.ctr.currentEntry.keywords.append("chair")
        self.ctr.currentEntry.keywords.append("table")
        self.ctr.view.drawEntry = MagicMock()
        self.ctr.model.updateNameOfEntry = MagicMock()
        self.ctr.model.updateContentOfEntry= MagicMock()
        self.ctr.model.addEntry = MagicMock()
        self.ctr.model.hasEntry= MagicMock()

    def tearDown(self):
        pass

    def testEntryNameChangeAction(self):
        '''Checks if the right method of model is called'''
        self.ctr.entryNameChangeAction("roofs")
        self.ctr.model.updateNameOfEntry.assert_called_with(self.ctr.currentEntry, "roofs")
        self.assertEqual("roofs", self.ctr.currentEntry.name)
        self.ctr.view.drawEntry.assert_called_with(self.ctr.currentEntry)
    
    def testEntryDescriptionChangeAction(self):
        '''Checks if the right method of model is called'''
        self.ctr.entryDescriptionChangeAction("new description")
        self.ctr.model.updateContentOfEntry.assert_called_with(self.ctr.currentEntry)
        self.assertEqual("new description", self.ctr.currentEntry.description)
        self.ctr.view.drawEntry.assert_called_with(self.ctr.currentEntry)

    def testEntryKeywordChangeAction(self):
        '''Checks if the right method of model is called'''
        self.ctr.entryKeywordChangeAction("window")
        self.ctr.model.updateContentOfEntry.assert_called_with(self.ctr.currentEntry)
        s = self.ctr.currentEntry.getStringFromKeywords(self.ctr.currentEntry.keywords)
        self.assertEqual("window", s)
        self.ctr.view.drawEntry.assert_called_with(self.ctr.currentEntry)
        
    def testNewEntryAction(self):
        '''Checks if an entry is added correctly'''
        self.ctr.model.hasEntry.return_value = False
        self.ctr.newEntryAction()
        self.assertEqual("enter name", self.ctr.currentEntry.name)
        self.ctr.model.addEntry.assert_called_with(self.ctr.currentEntry)
        self.ctr.view.drawEntry.assert_called_with(self.ctr.currentEntry)
        
    def testNewEntryActionIfEnterNameExists(self):
        '''In this test, the default enter name entry already existst'''
        self.ctr.model.hasEntry.side_effect = [True, True, False]
        self.ctr.newEntryAction()
        self.assertEqual("enter name2", self.ctr.currentEntry.name)
        self.ctr.model.addEntry.assert_called_with(self.ctr.currentEntry)
        self.ctr.view.drawEntry.assert_called_with(self.ctr.currentEntry)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testads']
    unittest.main()