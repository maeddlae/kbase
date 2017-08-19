'''
Created on 19 Aug 2017

@author: Mathias Bucher
'''
import unittest
from Tkinter import *
from view.VSearch import VSearch
from ctr.Log import Log
from mock import MagicMock
from model.ModelEntry import ModelEntry


class TestVSearch(unittest.TestCase):


    def setUp(self):
        self.log = Log("testlog.txt")
        self.log.add = MagicMock()
        
        self.root = Tk()
        self.root.title("kbase test")
        self.root.geometry("400x500")
        
        self.dummy = MagicMock()
        
        self.actionlist = {"showEntryAction" : self.dummy}
        
        self.vsearch = VSearch(self.root, self.log, self.actionlist)
        
        self.e1 = ModelEntry(self.log, "e1")
        self.e2 = ModelEntry(self.log, "e2")
        self.e3 = ModelEntry(self.log, "e3")
        self.e4 = ModelEntry(self.log, "e4")
        
        self.results = {"name" : [self.e1],
                        "keyword" : [self.e2],
                        "description" : [self.e3, self.e4]}

    def tearDown(self):
        pass

    def testDrawSearchResults(self):
        '''Tests whether all buttons are drawn'''
        self.vsearch.drawSearchResults(self.results)
        self.assertEqual(self.e1.name, self.vsearch.buttonName[0]["text"])
        self.assertEqual(self.e2.name, self.vsearch.buttonKeyword[0]["text"])
        self.assertEqual(self.e3.name, self.vsearch.buttonDescription[0]["text"])
        self.assertEqual(self.e4.name, self.vsearch.buttonDescription[1]["text"])

    def testButtonClicked(self):
        '''Tests whether the right buttons are clicked'''
        self.vsearch.drawSearchResults(self.results)
        self.vsearch.grid()
        self.root.update()
        
        # by name
        self.vsearch.buttonName[0].focus_force()
        self.vsearch.buttonName[0].invoke()
        self.dummy.assert_called_with(self.e1)      
        
        # by keyword
        self.vsearch.buttonKeyword[0].focus_force()
        self.vsearch.buttonKeyword[0].invoke()
        self.dummy.assert_called_with(self.e2)    
        
        # by description
        self.vsearch.buttonDescription[1].focus_force()
        self.vsearch.buttonDescription[1].invoke()
        self.dummy.assert_called_with(self.e4)      
        
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()