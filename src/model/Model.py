'''
Created on 24 Jul 2017

@author: Mathias Bucher
'''
from model.ModelEntry import ModelEntry

class Model():
    '''
    classdocs
    '''
    entries = []


    def __init__(self, log):
        '''
        Constructor
        '''
        self.log = log
        
        e = ModelEntry(self.log, "Bla")
        e.keywords.append("blabla")
        self.entries.append(e)
        
        e = ModelEntry(self.log, "Blu")
        e.keywords.append("blublu")
        self.entries.append(e)
        
        self.log.add(self.log.Info, __file__, "init" )
        
        
    def getEntry(self, keyword):
        foundEntry = None
        
        for e in self.entries:
            for k in e.keywords:
                if k == keyword and foundEntry == None:
                    foundEntry = e
            if e.title == keyword and foundEntry == None:
                    foundEntry = e
            
        if foundEntry!=None:
            self.log.add(self.log.Info, __file__, "entry found" )
        else:
            self.log.add(self.log.Info, __file__, "entry not found" )
            
        return foundEntry