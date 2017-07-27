'''
Created on 27 Jul 2017

@author: Mathias Bucher
'''

class ModelEntry(object):
    '''
    classdocs
    '''
    title = "title"
    text = "this is the text"
    keywords = []
    images = []
    files = []

    def __init__(self, log, title):
        '''
        Constructor
        '''
        self.log = log
        self.title = title
        
        self.log.add(self.log.Info, __file__, "init: " + title)