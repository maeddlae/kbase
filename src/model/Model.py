'''
Created on 24 Jul 2017

@author: Mathias Bucher
'''
from model.ModelEntry import ModelEntry

class Model():
    '''
    classdocs
    '''

    def __init__(self, log):
        '''
        Constructor
        '''
        self.log = log
        
        self.entries = []
        
        cars = ModelEntry(self.log, "cars")
        cars.keywords.append("BMW")
        cars.keywords.append("Volvo")
        self.entries.append(cars)
        
        ships = ModelEntry(self.log, "ships")
        ships.keywords.append("Queen Mary")
        ships.keywords.append("Santa Maria")
        self.entries.append(ships)
        
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