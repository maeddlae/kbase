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
        self.dummy2 = MagicMock()
        self.dummy3 = MagicMock()
        self.dummy4 = MagicMock()
        
        self.actionlist = {"searchAction" : self.dummy,
                           "newAction" : self.dummy2,
                           "deleteAction" : self.dummy4,
                           "closedAction" : self.dummy3}
        
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

    def testButtonAddClick(self):
        '''Tests whether the right method is called when user clicks add button'''
        self.vmenubar.draw()
        self.vmenubar.grid()
        self.root.update()
        self.vmenubar.buttonNew.focus_force()
        self.vmenubar.buttonNew.invoke()
        self.dummy2.assert_called_once()
        
    def testButtonClose(self):
        '''Tests whether the close button visibiliy is handled correctly'''
        self.vmenubar.draw()
        self.vmenubar.grid()
        self.root.update()
        
        # button is disabled by default, so it should not be clickable
        self.vmenubar.buttonClose.focus_force()
        self.vmenubar.buttonClose.invoke()
        self.dummy3.assert_not_called()
        
        # enable button and test again
        self.vmenubar.enableButtonClose()
        self.root.update()
        self.vmenubar.buttonClose.invoke()
        self.dummy3.assert_called_once()
        
        # disable button and test again
        self.dummy3.reset_mock() # reset mock, because call of last time is stored
        self.vmenubar.disableButtonClose()
        self.root.update()
        self.vmenubar.buttonClose.invoke()
        self.dummy3.assert_not_called()
        
    def testButtonDelete(self):
        '''Tests functionality and visibility of delete button'''
        self.vmenubar.draw()
        self.vmenubar.grid()
        self.root.update()
        
        # button is disabled by default, so it should not be clickable
        self.vmenubar.buttonDelete.focus_force()
        self.vmenubar.buttonDelete.invoke()
        self.dummy4.assert_not_called()
        
        # enable button and test again
        self.vmenubar.enableButtonDelete()
        self.root.update()
        self.vmenubar.buttonDelete.invoke()
        self.dummy4.assert_called_once()
        
        # disable button and test again
        self.dummy4.reset_mock() # reset mock, because call of last time is stored
        self.vmenubar.disableButtonDelete()
        self.root.update()
        self.vmenubar.buttonDelete.invoke()
        self.dummy4.assert_not_called()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()