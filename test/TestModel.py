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
        self.model.entries.append(self.fruits)
        self.model.entries.append(self.legumes)
        pass


    def tearDown(self):
        pass

    def testGetEntryByKeyword(self):
        exp = self.fruits
        act = self.model.getEntry("melon")
        self.assertEqual(exp,act)

    def testGetEntryByName(self):
        exp = self.legumes
        act = self.model.getEntry("legumes")
        self.assertEqual(exp,act)

    def testGetEntryIfNotExists(self):
        exp = None
        act = self.model.getEntry("planes")
        self.assertEqual(exp,act)
