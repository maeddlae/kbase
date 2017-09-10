'''
Created on 27 Jul 2017

@author: Mathias Bucher
'''
from model.Model import Model
from model.ModelEntry import ModelEntry
from ctr.Log import Log
import unittest
from mock import MagicMock
import os


class TestModel(unittest.TestCase):
    dbPath = "ModelTestDatabase.db"
    newDbPath = "newDatabase.db"

    def setUp(self):
        self.log = Log("testlog.txt")
        self.log.add = MagicMock()
        self.model = Model(self.log, self.dbPath)
        
        self.fruits = ModelEntry(self.log, "fruits")
        self.fruits.tags.append("apple")
        self.fruits.tags.append("melon")
        self.fruits.text = "This entry is about fruit"
        self.legumes = ModelEntry(self.log, "legumes")
        self.legumes.tags.append("tomato")
        self.cars = ModelEntry(self.log, "cars")
        self.cars.tags.append("mustang")
        self.cars.tags.append("volvo")
        self.cars.text = "This entry is about cars"
        
        self.model.db.addEntry(self.fruits)
        self.model.db.addEntry(self.legumes)
        self.model.foundEntries["name"].append(self.cars)
        self.model.foundEntries["description"].append(self.fruits)
        self.model.foundEntries["tag"].append(self.legumes)
        self.model.openedEntries.append(self.fruits)
        self.model.openedEntries.append(self.legumes)

    def tearDown(self):
        if os.path.exists(self.dbPath):
            os.remove(self.dbPath)
        if os.path.exists(self.newDbPath):
            os.remove(self.newDbPath)

    def testSetDatabase(self):
        '''Tests whether database can be changed'''
        e1 = ModelEntry(self.log, "e1" )
        self.model.setDatabase(self.newDbPath)
        self.model.addEntry(e1)
        
        self.assertFalse(self.model.hasEntry(self.fruits))
        self.assertTrue(self.model.hasEntry(e1))

    def testGetEntryByTag(self):
        exp = self.fruits
        act = self.model.getEntries("melon")["tag"][0]
        
        self.assertEqual(exp.name, act.name)
        self.assertEqual(exp.description, act.description)
        self.assertSequenceEqual(exp.tags, act.tags, str)

    def testGetEntryByName(self):
        exp = self.legumes
        act = self.model.getEntries("legumes")["name"][0]
        
        self.assertEqual(exp.name, act.name)
        self.assertEqual(exp.description, act.description)
        self.assertSequenceEqual(exp.tags, act.tags, str)

    def testGetEntryIfNotExists(self):
        act = self.model.getEntries("muha")
        self.assertEqual(act["name"].__len__(), 0)
        self.assertEqual(act["tag"].__len__(), 0)
        self.assertEqual(act["description"].__len__(), 0)
        
    def testUpdateNameOfEntry(self):  
        '''Checks only if the right method of db is called'''
        self.model.db.updateNameOfEntry = MagicMock()
        self.model.updateNameOfEntry(self.cars, "clocks")
        self.model.db.updateNameOfEntry.assert_called_with(self.cars, "clocks")
    
    def testUpdateContentOfEntry(self):
        '''Checks only if the right method of db is called'''
        self.model.db.updateEntry = MagicMock()
        self.model.updateContentOfEntry(self.cars)
        self.model.db.updateEntry.assert_called_with(self.cars)
    
    def testAddEntry(self):
        '''Checks only if the right method of db is called'''
        entry = ModelEntry(self.log, "new entry")
        self.model.db.addEntry = MagicMock()
        self.model.addEntry(entry)
        self.model.db.addEntry.assert_called_with(entry)
    
    def testRemoveEntry(self):
        '''Checks only if the right method of db is called'''
        entry = ModelEntry(self.log, "new entry")
        self.model.db.removeEntry = MagicMock()
        self.model.removeEntry(entry)
        self.model.db.removeEntry.assert_called_with(entry)
        
    def testGetOpenedEntry(self):
        '''Tests if right entry is returned'''
        exp = self.fruits
        act = self.model.getOpenedEntry(exp.name)
        self.assertEqual(exp, act)
        
    def testGetFoundEntry(self):
        '''Tests if right entry is returned'''
        exp = self.fruits
        act = self.model.getFoundEntry(exp.name)
        self.assertEqual(exp, act)
        exp = self.legumes
        act = self.model.getFoundEntry(exp.name)
        self.assertEqual(exp, act)
        exp = self.cars
        act = self.model.getFoundEntry(exp.name)
        self.assertEqual(exp, act)
        exp = None
        act = self.model.getFoundEntry("muhaa")
        self.assertEqual(exp, act)
