'''
Created on 27 Jul 2017

@author: Mathias Bucher
'''

class ModelEntry():
    '''
    Represents an entry and contains all its data.
    '''

    def __init__(self, log, name):
        '''
        Constructor
        '''
        self.log = log
        self.name = name
        self.description = "This is the description"
        self.keywords = []
        self.images = []
        self.files = []
        
        self.log.add(self.log.Info, __file__, "init: " + name)