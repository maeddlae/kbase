'''
Created on 14 Aug 2017

@author: Mathias Bucher
'''
import unittest
from mock import MagicMock
from model.ModelEntry import ModelEntry
from ctr.Log import Log


class TestModelEntry(unittest.TestCase):


    def setUp(self):
        self.log = Log("testlog.txt")
        self.log.add = MagicMock()
        
        self.entry = ModelEntry(self.log, "testentry")


    def tearDown(self):
        pass

    def testGetStringFromKeywords(self):
        exp = "asdf, sd swef , a a,  b b, "
        inp = ["asdf", "sd swef ", "a a", " b b", ""]
        act = self.entry.getStringFromKeywords(inp)
        self.assertEqual(exp, act)


    def testGetKeywordsFromString(self):
        exp = ["bla bla", "blu", " bleble", ""]
        inp = "bla bla, blu,  bleble, "
        act = self.entry.getKeywordsFromString(inp)
        self.assertSequenceEqual(exp,act,str)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()