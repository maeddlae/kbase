'''
Created on 24 Aug 2017

@author: Mathias Bucher
'''
import unittest
from mock import MagicMock
import os
from model.ConfigFile import ConfigFile
from ctr.Log import Log

class TestConfigFile(unittest.TestCase):
    path = "testconfig.txt"
    pathNotExisting = "notexisting.txt"

    def setUp(self):
        self.log = Log("testlog.txt")
        self.log.add = MagicMock()
        
        self.cfgfile = ConfigFile( self.log, self.path)
        
        self.content = "a = sdf\nb = 123\n"
        self.file = open(self.path, "w+")
        self.file.write(self.content)
        self.file.close()


    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)
        if os.path.exists(self.pathNotExisting):
            os.remove(self.pathNotExisting)
        
    def testIfFileNotExists(self):
        '''Tests if a value is added correctly if file 
        does not exist'''
        _ = ConfigFile(self.log, self.pathNotExisting)
        self.assertTrue(os.path.exists(self.pathNotExisting))
            
    def testGetDict(self):
        '''Tests whether it returns the right dict'''
        inp = "a = sdfa asdf\n asdf = asdf =Asfd\n\nb=a\n"
        exp = {"a" : "sdfa asdf",
               " asdf" : "asdf =Asfd"}
        act = self.cfgfile.getDict(inp)
        
        self.log.add.assert_called()
        self.assertEqual(exp.__len__(), act.__len__())
        self.assertSequenceEqual(exp, act, str)

    def testSetValueIfNew(self):
        '''Adds a new value to config file'''
        exp = self.content
        exp += "c = muha\n"
        
        self.cfgfile.setValue("c", "muha")
        
        f = open(self.path, "r")
        act = f.read()
        f.close()
        self.assertEqual(exp, act)

    def testSetValueIfExists(self):
        '''Tests whether an existing value is updated
        correctly'''
        exp = self.content
        exp = exp.replace("sdf", "lkfndgf")
        
        self.cfgfile.setValue("a", "lkfndgf")
        
        f = open(self.path, "r")
        act = f.read()
        f.close()
        self.assertEqual(exp, act)
    
    def testGetValueIfExists(self):
        '''Tests whether an existing value can be 
        returned'''
        exp = "123"
        
        act = self.cfgfile.getValue("b")
        self.assertEqual(exp, act)
    
    def testGetValueIfNotExists(self):
        '''Sees what happens if a non existing value is 
        requested'''
        exp = None
        act = self.cfgfile.getValue("c")
        self.log.add.assert_called()
        self.assertEqual(exp, act)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()