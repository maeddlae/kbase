'''
Created on 27 Jul 2017

@author: Mathias Bucher
'''

class ModelEntry():
    '''
    classdocs
    '''

    def __init__(self, log, title):
        '''
        Constructor
        '''
        self.log = log
        self.title = title
        self.text = "This is the text"
        self.keywords = []
        self.images = []
        self.files = []
        
        self.log.add(self.log.Info, __file__, "init: " + title)