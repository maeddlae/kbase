'''
Created on 17 Aug 2017

@author: Mathias Bucher
'''
import unittest
from Tkinter import *
from view.VMenubar import VMenubar
from ctr.Log import Log
from mock import MagicMock


class TestVMenubar(unittest.TestCase):


    def setUp(self):
        self.log = Log("testlog.txt")
        self.log.add = MagicMock()
        
        self.root = Tk()
        self.root.title("kbase test")
        self.root.geometry("400x500")
        
        self.dummy = MagicMock()
        
        self.actionlist = {"searchAction" : self.dummy}
        
        self.vmenubar = VMenubar(self.root, self.log, self.actionlist)

    def tearDown(self):
        pass

    def testButtonGoClick(self):
        '''Tests whether the right method is called when user clicks go button'''
        self.vmenubar.draw()
        self.vmenubar.grid()
        self.root.update()
        self.vmenubar.entrySearchText.set("searchtext")
        self.vmenubar.buttonGo.focus_force()
        self.vmenubar.buttonGo.invoke()
        self.dummy.assert_called_with("searchtext")

    def testReturnPressOnSearch(self):
        '''Tests whether the right method is called when user hits 
        Return key at search field'''
        self.vmenubar.draw()
        self.vmenubar.grid()
        self.root.update()
        self.vmenubar.entrySearchText.set("searchtext")
        self.vmenubar.entrySearch.focus_force()
        self.vmenubar.entrySearch.event_generate("<Return>")
        self.dummy.assert_called_with("searchtext")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()