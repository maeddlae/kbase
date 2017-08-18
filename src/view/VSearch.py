'''
Created on 12 Aug 2017

@author: Mathias Bucher
'''
from Tkinter import *

class VSearch(Frame):
    '''
    Shows search results
    '''


    def __init__(self, root, log):
        '''
        Constructor
        '''
        Frame.__init__(self, root)
        self.log = log
        self.log.add(self.log.Info, __file__, "init" )
        
    def drawSearchResults(self, results):
        pass