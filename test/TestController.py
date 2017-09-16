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
import os
from mock import mock_open, patch
import copy


class TestController(unittest.TestCase):
    dbPath = "testdb.db"
    configPath = "config.txt"
    changePath = "adsfasd.txt"
    testPath = os.path.dirname(os.path.realpath(__file__))
    testWordName = "testword.docx"
    testWordPath = testPath + "\\" + testWordName
    testImageName = "testimage.jpg"
    testImagePath =  testPath + "\\" + testImageName

    def setUp(self):
        self.log = Log("testlog.txt")
        self.log.add = MagicMock()
        
        f = open(self.testImagePath, "rb")
        self.testImageStream = f.read()
        f.close()
        
        f = open(self.configPath, "w+")
        f.write("databasepath = " + self.dbPath + "\n")
        f.close()
        
        f = open(self.testWordPath, "rb")
        self.testWordStream = f.read()
        f.close()
        
        self.ctr = Controller( self.log, self.configPath )
        self.ctr.model.currentEntry = ModelEntry(self.log, "furniture")
        self.ctr.model.currentEntry.description = "This is the description of furniture"
        self.ctr.model.currentEntry.tags.append("chair")
        self.ctr.model.currentEntry.tags.append("table")
        self.ctr.model.currentEntry.images[self.testImageName] = self.testImageStream
        self.ctr.model.currentEntry.files[self.testWordName] = self.testWordStream
        self.ctr.view.drawEntry = MagicMock()
        self.ctr.view.drawSearch = MagicMock()
        self.ctr.view.removeEntry = MagicMock()
        self.ctr.view.removeSearch = MagicMock()
        self.ctr.view.setDeleteButton = MagicMock()
        self.ctr.view.removeEntry = MagicMock()
        self.ctr.view.changeDbPath = MagicMock()
        self.ctr.view.showNewImageSelectDialog = MagicMock()
        self.ctr.view.showNewFileSelectDialog = MagicMock()
        self.ctr.model.updateNameOfEntry = MagicMock()
        self.ctr.model.updateContentOfEntry= MagicMock()
        self.ctr.model.addEntry = MagicMock()
        self.ctr.model.hasEntry= MagicMock()
        self.ctr.model.getEntries = MagicMock()
        self.ctr.model.removeEntry = MagicMock()
        self.ctr.config.setValue = MagicMock()
        os.startfile = MagicMock()

    def tearDown(self):
        if os.path.exists(self.dbPath):
            os.remove(self.dbPath)
        if os.path.exists(self.configPath):
            os.remove(self.configPath)
        if os.path.exists(self.changePath):
            os.remove(self.changePath)
        self.ctr.view.tabs.grid()
        self.ctr.view.menubar.grid()
        self.ctr.view.dbPath.grid()
        self.ctr.view.root.update()
        self.ctr.view.root.destroy()
            
    def testChangePathAction(self):
        '''Tests only if right method are called'''
        exp = self.changePath
        self.ctr.changePathAction(exp)
        self.assertEqual(exp, self.ctr.dbPath)
        self.ctr.config.setValue.assert_called_with(self.ctr.configDataBase, exp)
        self.assertEqual(exp, self.ctr.model.db.path)
        self.ctr.view.changeDbPath.assert_called_with(exp)
            
    def testIfGivesRightDbPAth(self):
        '''Tests whether controller gives right db path 
        to model'''
        self.assertEqual(self.dbPath, self.ctr.model.db.path)

    def testEntryChangeAction(self):
        '''Checks if the right method of model is called'''
        self.ctr.entryChangeAction("roofs", "new description")
        self.ctr.model.updateNameOfEntry.assert_called_with(self.ctr.model.currentEntry, "roofs")
        self.ctr.model.updateContentOfEntry.assert_called_with(self.ctr.model.currentEntry)
        self.assertEqual("roofs", self.ctr.model.currentEntry.name)
        self.assertEqual("new description", self.ctr.model.currentEntry.description)
        self.ctr.view.removeEntry.assert_called_with(self.ctr.model.currentEntry)
        self.ctr.view.drawEntry.assert_called_with(self.ctr.model.currentEntry)

    def testNewEntryAction(self):
        '''Checks if an entry is added correctly'''
        self.ctr.model.hasEntry.return_value = False
        self.ctr.newEntryAction()
        self.assertEqual("enter name", self.ctr.model.currentEntry.name)
        self.ctr.model.addEntry.assert_called_with(self.ctr.model.currentEntry)
        self.ctr.view.drawEntry.assert_called_with(self.ctr.model.currentEntry)
        
    def testNewEntryActionIfEnterNameExists(self):
        '''In this test, the default enter name entry already existst'''
        self.ctr.model.hasEntry.side_effect = [True, True, False]
        self.ctr.newEntryAction()
        self.assertEqual("enter name2", self.ctr.model.currentEntry.name)
        self.ctr.model.addEntry.assert_called_with(self.ctr.model.currentEntry)
        self.ctr.view.drawEntry.assert_called_with(self.ctr.model.currentEntry)
        
    def testSearchActionMultipleMatches(self):
        '''Tests whether the search action calls the right methods'''
        e1 = ModelEntry(self.log, "hit1")
        e2 = ModelEntry(self.log, "hit2")
        e3 = ModelEntry(self.log, "hit3")
        e4 = ModelEntry(self.log, "hit4")
        
        found = {"name" : [e1, e2],
                 "tag" : [e3],
                 "description" : [e4]}
        
        self.ctr.model.getEntries.return_value = found
        self.ctr.searchAction("search")
        self.ctr.model.getEntries.assert_called_with("search")
        self.ctr.view.drawSearch.assert_called_with(found)
        
    def testSearchActionSingleMatch(self):
        '''Tests whether the search action calls the right methods'''
        e1 = ModelEntry(self.log, "hit1")
        
        found = {"name" : [],
                 "tag" : [e1],
                 "description" : []}
        
        self.ctr.model.getEntries.return_value = found
        self.ctr.searchAction("search")
        self.ctr.model.getEntries.assert_called_with("search")
        self.ctr.view.drawSearch.assert_called_with(found)
        
    def testEntryClickedInVSearch(self):
        '''Tests whether the search action calls the right methods'''
        e = ModelEntry(self.log, "entry")
        self.ctr.model.foundEntries["name"].append(e)
        
        self.ctr.entryClickedInVSearch("entry")
        self.assertEqual(e, self.ctr.model.foundEntries["name"][0])
        self.ctr.view.drawEntry.assert_called_with(e)
        
    def testCloseTabAction(self):
        # close entry
        e = ModelEntry(self.log, "entry")
        self.ctr.model.currentEntry = e
        self.ctr.model.openedEntries.append(e)
        self.ctr.closeTabAction()
        self.assertEqual(0, self.ctr.model.openedEntries.__len__())
        self.ctr.view.removeEntry.assert_called_with(e)    
        
        # close search
        self.ctr.isSearchActive = True
        self.ctr.closeTabAction()
        self.ctr.view.removeSearch.assert_called_once()
        
        
    def testTabChangeAction(self):
        e1 = ModelEntry(self.log, "e1")
        e2 = ModelEntry(self.log, "e2")
        
        self.ctr.model.openedEntries.append(e1)
        self.ctr.model.openedEntries.append(e2)
        self.ctr.model.currentEntry = e1
        self.ctr.tabChangeAction(e2.name, False)
        self.assertEqual(e2, self.ctr.model.currentEntry)
        self.assertFalse(self.ctr.isSearchActive)
        self.ctr.view.setDeleteButton.assert_called_with(True)
        
        self.ctr.tabChangeAction(None, True)
        self.assertEqual(e2, self.ctr.model.currentEntry)
        self.assertTrue(self.ctr.isSearchActive)
        self.ctr.view.setDeleteButton.assert_called_with(False)
        
    def testDeleteEntryAction(self):
        self.ctr.model.currentEntry = ModelEntry(self.log, "e1")
        self.ctr.deleteEntryAction()
        self.ctr.model.removeEntry.assert_called_once_with(self.ctr.model.currentEntry)
        self.ctr.view.removeEntry.assert_called_once_with(self.ctr.model.currentEntry)
        
    def testNewImageAction(self):
        self.ctr.newImageAction()
        self.ctr.view.showNewImageSelectDialog.assert_called_once()
        
    def testNewTagAction(self):
        newTag = "asdfa"
        exp = self.ctr.model.currentEntry.tags
        exp.append(newTag)
        
        self.ctr.newTagAction(newTag)
        
        act = self.ctr.model.currentEntry.tags
        self.assertEqual(exp.__len__(), act.__len__())
        self.assertSequenceEqual(exp, act)
        self.ctr.model.updateContentOfEntry.assert_called_once_with(self.ctr.model.currentEntry)
        self.ctr.view.removeEntry.assert_called_once_with(self.ctr.model.currentEntry)
        self.ctr.view.drawEntry.assert_called_once_with(self.ctr.model.currentEntry)
        
    def testDeleteTagAction(self):
        tagToDelete = self.ctr.model.currentEntry.tags[0]
        exp = copy.copy(self.ctr.model.currentEntry.tags)
        exp.remove(tagToDelete)
        
        self.ctr.deleteTagAction(tagToDelete)
        
        act = self.ctr.model.currentEntry.tags
        self.assertEqual(exp.__len__(), act.__len__())
        self.assertSequenceEqual(exp, act)
        self.ctr.model.updateContentOfEntry.assert_called_once_with(self.ctr.model.currentEntry)
        self.ctr.view.removeEntry.assert_called_once_with(self.ctr.model.currentEntry)
        self.ctr.view.drawEntry.assert_called_once_with(self.ctr.model.currentEntry)
        
    def testDeleteImageAction(self):
        imageToDelete = self.testImageName
        exp = copy.copy(self.ctr.model.currentEntry.images)
        del exp[imageToDelete]
        
        self.ctr.deleteImageAction(imageToDelete)
        
        act = self.ctr.model.currentEntry.images
        self.assertEqual(exp.__len__(), act.__len__())
        self.assertSequenceEqual(exp, act)
        self.ctr.model.updateContentOfEntry.assert_called_once_with(self.ctr.model.currentEntry)
        self.ctr.view.removeEntry.assert_called_once_with(self.ctr.model.currentEntry)
        self.ctr.view.drawEntry.assert_called_once_with(self.ctr.model.currentEntry)

    def testNewFileAction(self):
        self.ctr.newFileAction()
        self.ctr.view.showNewFileSelectDialog.assert_called_once()
        
    def testDeleteFileAction(self):
        fileToDelete = self.testWordName
        exp = copy.copy(self.ctr.model.currentEntry.files)
        del exp[fileToDelete]
        
        self.ctr.deleteFileAction(fileToDelete)
        
        act = self.ctr.model.currentEntry.files
        self.assertEqual(exp.__len__(), act.__len__())
        self.assertSequenceEqual(exp, act)
        self.ctr.model.updateContentOfEntry.assert_called_once_with(self.ctr.model.currentEntry)
        self.ctr.view.removeEntry.assert_called_once_with(self.ctr.model.currentEntry)
        self.ctr.view.drawEntry.assert_called_once_with(self.ctr.model.currentEntry)

    def testAddFile(self):
        filename = self.configPath
        fullPath = os.path.abspath(filename)
        data = "some data"
        
        mopen = MagicMock()
        with patch('__builtin__.open', mopen):
            manager = mopen.return_value.__enter__.return_value
            manager.read.return_value = data
            self.ctr.addFile(fullPath)
            
        mopen.assert_called_once_with(fullPath, "rb")
        exp = filename
        act = next(iter(self.ctr.model.currentEntry.files))
        self.assertEqual(exp, act)
        self.ctr.model.updateContentOfEntry.assert_called_once_with(self.ctr.model.currentEntry)
        self.ctr.view.removeEntry.assert_called_once_with(self.ctr.model.currentEntry)
        self.ctr.view.drawEntry.assert_called_once_with(self.ctr.model.currentEntry)
        
    def testAddImage(self):
        filename = self.configPath
        data = "some data"
        
        mopen = MagicMock()
        with patch('__builtin__.open', mopen):
            manager = mopen.return_value.__enter__.return_value
            manager.read.return_value = data
            self.ctr.addImage(filename)
            
        mopen.assert_called_once_with(filename, "rb")
        self.ctr.model.updateContentOfEntry.assert_called_once_with(self.ctr.model.currentEntry)
        self.ctr.view.removeEntry.assert_called_once_with(self.ctr.model.currentEntry)
        self.ctr.view.drawEntry.assert_called_once_with(self.ctr.model.currentEntry)
        
    def testNewFileOrImageSelectedAction(self):
        self.ctr.addFile = MagicMock()
        self.ctr.addImage = MagicMock()
        self.ctr.model.currentEntry.isSupportedImageFile = MagicMock()
        
        # test add image if exists
        filename = self.testImageName
        self.ctr.model.currentEntry.isSupportedImageFile.return_value = True
        self.ctr.newFileOrImageSelectedAction(filename)
        self.ctr.addImage.assert_called_once_with(filename)
        self.ctr.addFile.assert_not_called()
        self.ctr.view.removeEntry.assert_called_once_with(self.ctr.model.currentEntry)
        self.ctr.view.drawEntry.assert_called_once_with(self.ctr.model.currentEntry)
        
        # test add file if exists
        filename = self.testWordName
        self.ctr.addFile.reset_mock()
        self.ctr.addImage.reset_mock()
        self.ctr.view.removeEntry.reset_mock()
        self.ctr.view.drawEntry.reset_mock()
        self.ctr.model.currentEntry.isSupportedImageFile.return_value = False
        self.ctr.newFileOrImageSelectedAction(filename)
        self.ctr.addImage.assert_not_called()
        self.ctr.addFile.assert_called_once_with(filename)
        self.ctr.view.removeEntry.assert_called_once_with(self.ctr.model.currentEntry)
        self.ctr.view.drawEntry.assert_called_once_with(self.ctr.model.currentEntry)
        
        # test add file if not exists
        filename = "blublu.adf"
        self.ctr.addFile.reset_mock()
        self.ctr.addImage.reset_mock()
        self.ctr.view.removeEntry.reset_mock()
        self.ctr.view.drawEntry.reset_mock()
        self.ctr.model.currentEntry.isSupportedImageFile.return_value = False
        self.ctr.newFileOrImageSelectedAction(filename)
        self.ctr.addImage.assert_not_called()
        self.ctr.addFile.assert_not_called()
        self.ctr.view.removeEntry.assert_called_once_with(self.ctr.model.currentEntry)
        self.ctr.view.drawEntry.assert_called_once_with(self.ctr.model.currentEntry)

    def testOpenFileAction(self):
        self.ctr.openFileAction(self.testWordName)
        os.startfile.assert_called_with(os.path.abspath(self.testWordName))
        self.ctr.openFileAction(self.testImageName)
        os.startfile.assert_called_with(os.path.abspath(self.testImageName))
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testads']
    unittest.main()