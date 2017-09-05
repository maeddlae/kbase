'''
Created on 25 Aug 2017

@author: Mathias Bucher
'''
import unittest
from view.View import View
from ctr.Log import Log
from mock import MagicMock
from view.VMenubar import VMenubar
from view.VTab import VTab
import Tkinter, tkFileDialog


class TestView(unittest.TestCase):


    def setUp(self):
        self.log = Log("testlog.txt")
        self.log.add = MagicMock()

        self.dummy1 = MagicMock()
        self.actions = {"fileSelectedAction" : self.dummy1}
        self.dbPath = "arxads"
        
        self.view = View(log=self.log, dbPath=self.dbPath, actions=self.actions)
        self.view.menubar.enableButtonClose = MagicMock()
        self.view.menubar.enableButtonDelete = MagicMock()
        self.view.tabs.addEntry = MagicMock()
        self.view.tabs.grid = MagicMock()
        self.view.tabs.setSearch = MagicMock()
        self.view.tabs.removeEntry = MagicMock()
        self.view.tabs.hasTabs = MagicMock()
        self.view.menubar.disableButtonClose = MagicMock()
        self.view.menubar.disableButtonDelete = MagicMock()
        self.view.tabs.removeSearch = MagicMock()
        self.view.dbPath.changePath = MagicMock()
        
        self.askopenfilenameBackup = tkFileDialog.askopenfilename
        tkFileDialog.askopenfilename = MagicMock()

    def tearDown(self):
        tkFileDialog.askopenfilename = self.askopenfilenameBackup

    def testDrawEntry(self):
        e = "test"
        self.view.drawEntry(e)
        self.view.menubar.enableButtonClose.assert_called_once()
        self.view.menubar.enableButtonDelete.assert_called_once()
        self.view.tabs.addEntry.assert_called_once_with(e)
        self.view.tabs.grid.assert_called()
    
    def testDrawSearch(self):
        e = "test"
        self.view.drawSearch(e)
        self.view.menubar.enableButtonClose.assert_called_once()
        self.view.tabs.setSearch(e)
        self.view.tabs.grid.assert_called()
        
    def testRemoveEntry(self):
        e = "test"
        self.view.tabs.hasTabs.return_value = True
        self.view.removeEntry(e)
        self.view.tabs.removeEntry.assert_called_with(e)
        
        self.view.tabs.hasTabs.return_value = False
        self.view.removeEntry(e)
        self.view.tabs.removeEntry.assert_called_with(e)
        self.view.menubar.disableButtonClose.assert_called_once()
        self.view.menubar.disableButtonDelete.assert_called_once()

    def testRemoveSearch(self):
        self.view.tabs.hasTabs.return_value = True
        self.view.removeSearch()
        self.view.tabs.removeSearch.assert_called()
        
        self.view.tabs.hasTabs.return_value = False
        self.view.removeSearch()
        self.view.menubar.disableButtonClose.assert_called_once()
            
    def testSetDeleteButton(self):
        self.view.setDeleteButton(True)
        self.view.menubar.enableButtonDelete.assert_called_once()
        self.view.menubar.disableButtonDelete.assert_not_called()
        
        self.view.menubar.enableButtonDelete.reset_mock()
        self.view.setDeleteButton(False)
        self.view.menubar.enableButtonDelete.assert_not_called()
        self.view.menubar.disableButtonDelete.assert_called_once()
            
    def testChangeDbPath(self):
        newPath = "dsaf"
        self.view.changeDbPath(newPath)
        self.view.dbPath.changePath.assert_called_once_with(newPath)
        
    def testShowFileDialog(self):
        filename = "filenameblabla"
        tkFileDialog.askopenfilename.return_value = filename
        self.view.showFileDialog()
        tkFileDialog.askopenfilename.assert_called_once()
        self.dummy1.assert_called_once_with(filename)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()