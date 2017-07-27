'''
Created on 27 Jul 2017

@author: Mathias Bucher
'''
from model.Model import Model
from ctr.Log import Log
import unittest
from mock import MagicMock


class TestModel(unittest.TestCase):

    def setUp(self):
        
        self.log = Log("testlog.txt")
        self.log.add = MagicMock()
        self.model = Model(self.log)
        pass


    def tearDown(self):
        pass


    def testName(self):
        
        pass
