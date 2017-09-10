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
    
    def testIsSupportedImageFile(self):
        self.assertTrue(self.entry.isSupportedImageFile("asdf/blublu/bloblo.jpg"))
        self.assertTrue(self.entry.isSupportedImageFile("bloblo.png"))
        self.assertFalse(self.entry.isSupportedImageFile("asdf/bloblo.aaa"))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()