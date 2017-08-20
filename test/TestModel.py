'''
Created on 27 Jul 2017

@author: Mathias Bucher
'''
from model.Model import Model
from model.ModelEntry import ModelEntry
from ctr.Log import Log
import unittest
from mock import MagicMock


class TestModel(unittest.TestCase):

    def setUp(self):
        self.log = Log("testlog.txt")
        self.log.add = MagicMock()
        self.model = Model(self.log, "ModelTestDatabase.db")
        
        self.fruits = ModelEntry(self.log, "fruits")
        self.fruits.keywords.append("apple")
        self.fruits.keywords.append("melon")
        self.fruits.text = "This entry is about fruit"
        self.legumes = ModelEntry(self.log, "legumes")
        self.legumes.keywords.append("tomato")
        self.cars = ModelEntry(self.log, "fruits")
        self.cars.keywords.append("apple")
        self.cars.keywords.append("melon")
        self.cars.text = "This entry is about fruit"
        
        self.model.db.addEntry(self.fruits)
        self.model.db.addEntry(self.legumes)
        pass

    def tearDown(self):
        pass

    def testGetEntryByKeyword(self):
        exp = self.fruits
        act = self.model.getEntries("melon")["keyword"][0]
        
        self.assertEqual(exp.name, act.name)
        self.assertEqual(exp.description, act.description)
        self.assertSequenceEqual(exp.keywords, act.keywords, str)

    def testGetEntryByName(self):
        exp = self.legumes
        act = self.model.getEntries("legumes")["name"][0]
        
        self.assertEqual(exp.name, act.name)
        self.assertEqual(exp.description, act.description)
        self.assertSequenceEqual(exp.keywords, act.keywords, str)

    def testGetEntryIfNotExists(self):
        act = self.model.getEntries("muha")
        self.assertEqual(act["name"].__len__(), 0)
        self.assertEqual(act["keyword"].__len__(), 0)
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
        
        
