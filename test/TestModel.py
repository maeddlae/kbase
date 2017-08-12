'''
Created on 27 Jul 2017

@author: Mathias Bucher
'''
from model.Model import Model
from model.Model import ModelEntry
from ctr.Log import Log
import unittest
from mock import MagicMock


class TestModel(unittest.TestCase):

    def setUp(self):
        self.log = Log("testlog.txt")
        self.log.add = MagicMock()
        self.model = Model(self.log)
        
        self.fruits = ModelEntry(self.log, "fruits")
        self.fruits.keywords.append("apple")
        self.fruits.keywords.append("melon")
        self.fruits.text = "This entry is about fruit"
        self.legumes = ModelEntry(self.log, "legumes")
        self.legumes.keywords.append("tomato")
        
        self.model.db.addEntry(self.fruits)
        self.model.db.addEntry(self.legumes)
        pass

    def tearDown(self):
        pass

    def testGetEntryByKeyword(self):
        exp = self.fruits
        act = self.model.getEntry("melon")
        
        self.assertEqual(exp.name, act.name)
        self.assertEqual(exp.description, act.description)
        self.assertSequenceEqual(exp.keywords, act.keywords, str)

    def testGetEntryByName(self):
        exp = self.legumes
        act = self.model.getEntry("legumes")
        
        self.assertEqual(exp.name, act.name)
        self.assertEqual(exp.description, act.description)
        self.assertSequenceEqual(exp.keywords, act.keywords, str)

    def testGetEntryIfNotExists(self):
        act = self.model.getEntry("muha")
        self.assertEqual(act, None)
