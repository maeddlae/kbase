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
        
    def getStringFromKeywords(self, keywords):
        '''Puts all elements of keywords into a string, separated by comma and space'''
        s = ""
        last = keywords.__len__() - 1
        for i, k in enumerate(keywords):
            s += k
            if i < last:
                s += ", "
                    
        return s
    
    def getKeywordsFromString(self, string):
        '''Returns all ', ' separated keywords in a list'''
        return string.split(", ")