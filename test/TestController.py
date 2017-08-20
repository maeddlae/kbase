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
        self.ctr.view.drawSearch = MagicMock()
        self.ctr.view.removeEntry = MagicMock()
        self.ctr.view.removeSearch = MagicMock()
        self.ctr.view.setDeleteButton = MagicMock()
        self.ctr.view.removeEntry = MagicMock()
        self.ctr.model.updateNameOfEntry = MagicMock()
        self.ctr.model.updateContentOfEntry= MagicMock()
        self.ctr.model.addEntry = MagicMock()
        self.ctr.model.hasEntry= MagicMock()
        self.ctr.model.getEntries = MagicMock()
        self.ctr.model.removeEntry = MagicMock()

    def tearDown(self):
        pass

    def testEntryNameChangeAction(self):
        '''Checks if the right method of model is called'''
        self.ctr.entryNameChangeAction("roofs")
        self.ctr.model.updateNameOfEntry.assert_called_with(self.ctr.currentEntry, "roofs")
        self.assertEqual("roofs", self.ctr.currentEntry.name)
        self.ctr.view.removeEntry.assert_called_with(self.ctr.currentEntry)
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
        
    def testSearchActionMultipleMatches(self):
        '''Tests whether the search action calls the right methods'''
        e1 = ModelEntry(self.log, "hit1")
        e2 = ModelEntry(self.log, "hit2")
        e3 = ModelEntry(self.log, "hit3")
        e4 = ModelEntry(self.log, "hit4")
        
        found = {"name" : [e1, e2],
                 "keyword" : [e3],
                 "description" : [e4]}
        
        self.ctr.model.getEntries.return_value = found
        self.ctr.searchAction("search")
        self.ctr.model.getEntries.assert_called_with("search")
        self.ctr.view.drawSearch.assert_called_with(found)
        
    def testSearchActionSingleMatch(self):
        '''Tests whether the search action calls the right methods'''
        e1 = ModelEntry(self.log, "hit1")
        
        found = {"name" : [],
                 "keyword" : [e1],
                 "description" : []}
        
        self.ctr.model.getEntries.return_value = found
        self.ctr.searchAction("search")
        self.ctr.model.getEntries.assert_called_with("search")
        self.ctr.view.drawSearch.assert_called_with(found)
        
    def testEntryClickedInVSearch(self):
        '''Tests whether the search action calls the right methods'''
        e = ModelEntry(self.log, "entry")
        
        self.ctr.entryClickedInVSearch(e)
        self.assertEqual(e, self.ctr.model.activeEntries[0])
        self.ctr.view.drawEntry.assert_called_with(e)
        
    def testCloseTabAction(self):
        # close entry
        e = ModelEntry(self.log, "entry")
        self.ctr.currentEntry = e
        self.ctr.model.activeEntries.append(e)
        self.ctr.closeTabAction()
        self.assertEqual(0, self.ctr.model.activeEntries.__len__())
        self.ctr.view.removeEntry.assert_called_with(e)    
        
        # close search
        self.ctr.isSearchActive = True
        self.ctr.closeTabAction()
        self.ctr.view.removeSearch.assert_called_once()
        
        
    def testTabChangeAction(self):
        e1 = ModelEntry(self.log, "e1")
        e2 = ModelEntry(self.log, "e2")
        
        self.ctr.model.activeEntries.append(e1)
        self.ctr.model.activeEntries.append(e2)
        self.ctr.currentEntry = e1
        self.ctr.tabChangeAction(e2.name, False)
        self.assertEqual(e2, self.ctr.currentEntry)
        self.assertFalse(self.ctr.isSearchActive)
        self.ctr.view.setDeleteButton.assert_called_with(True)
        
        self.ctr.tabChangeAction(None, True)
        self.assertEqual(e2, self.ctr.currentEntry)
        self.assertTrue(self.ctr.isSearchActive)
        self.ctr.view.setDeleteButton.assert_called_with(False)
        
    def testDeleteEntryAction(self):
        self.ctr.currentEntry = ModelEntry(self.log, "e1")
        self.ctr.deleteEntryAction()
        self.ctr.model.removeEntry.assert_called_once_with(self.ctr.currentEntry)
        self.ctr.view.removeEntry.assert_called_once_with(self.ctr.currentEntry)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testads']
    unittest.main()