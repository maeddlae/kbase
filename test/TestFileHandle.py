'''
Created on 31 Aug 2017

@author: Mathias Bucher
'''
import unittest
from mock import MagicMock
from ctr.Log import Log
from model.FileHandle import FileHandle


class TestFileHandle(unittest.TestCase):


    def setUp(self):
        self.log = Log("testlog.txt")
        self.log.add = MagicMock()
        
        self.filehandle = FileHandle(self.log)
        
        x1 = bytearray([0x23, 0xAA, 0xBB, 0xCD])
        x2 = bytearray([0xAA, 0xBB, 0xAA, 0x12, 0xAA, 0xAA, 0xBB, 0xAA, 0xDC])
        x3 = bytearray([0x34, 0xAA, 0xBB, 0xBB, 0xAA, 0x56])
        x4 = bytearray([0x34, 0xAA, 0xBB, 0x56])
        self.x = [x1, x2, x3, x4]
        self.y = bytearray([0x23, 0xAA, 0xBB, 0xBB, 0xCD, 
                         0xAA, 0xBB, 0xAA, 
                         0xAA, 0xBB, 0xBB, 0xAA, 0x12, 0xAA, 0xAA, 0xBB, 0xBB, 0xAA, 0xDC,
                         0xAA, 0xBB, 0xAA,
                         0x34, 0xAA, 0xBB, 0xBB, 0xBB, 0xAA, 0x56,
                         0xAA, 0xBB, 0xAA,
                         0x34, 0xAA, 0xBB, 0xBB, 0x56,
                         0xAA, 0xBB, 0xAA])


    def tearDown(self):
        pass
    
    def testInsertSyncWords(self):
        exp = self.y
        act = self.filehandle.insertSyncWords(self.x)
        self.assertEqual(exp.__len__(), act.__len__())
        self.assertSequenceEqual(exp, act)
        
    def testRemoveSyncWords(self):
        exp = self.x
        act = self.filehandle.removeSyncWords(self.y)
        self.assertEqual(exp.__len__(), act.__len__())
        for e, a in zip(exp,act):
            self.assertEqual(e.__len__(), a.__len__())
            self.assertSequenceEqual(e, a)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()