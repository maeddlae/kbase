'''
Created on 25 Aug 2017

@author: Mathias Bucher
'''
import unittest
from Tkinter import *
from view.VDbPath import VDbPath
from ctr.Log import Log
from mock import MagicMock


class TestVDbPath(unittest.TestCase):


    def setUp(self):
        self.log = Log("testlog.txt")
        self.log.add = MagicMock()
        
        self.root = Tk()
        self.root.title("kbase test")
        self.root.geometry("400x500")
        
        self.dummy = MagicMock()
        
        self.actionlist = {"pathChangeAction" : self.dummy}
        
        self.vdbpath = VDbPath(self.root, self.log, self.actionlist)

    def tearDown(self):
        self.vdbpath.grid()
        self.root.update()
        self.root.destroy()

    def testDrawPathField(self):
        '''Tests whether database field is drawn correctly'''
        exp = "muhahah"
        self.vdbpath.draw(exp)
        act = self.vdbpath.dbPathEntryText.get()
        self.assertEqual(exp, act)
        
    def testChangePath(self):
        '''Changes the path once'''
        pathOld = "masdfa"
        exp = "afexs"
        
        self.vdbpath.draw(pathOld)
        self.vdbpath.changePath(exp)
        act = self.vdbpath.dbPathEntryText.get()
        self.assertEqual(exp, act)
        
    def testReturnClickAtPathField(self):
        '''Tests return click action'''
        oldPath = "asdfasex"
        self.vdbpath.draw(oldPath)
        self.vdbpath.grid()
        self.root.update()
        newPath = "amxraf,yserx"
        self.vdbpath.dbPathEntryText.set(newPath)
        self.vdbpath.dbPathEntry.focus_force()
        self.vdbpath.dbPathEntry.event_generate("<Return>")
        self.dummy.assert_called_with(newPath)
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()