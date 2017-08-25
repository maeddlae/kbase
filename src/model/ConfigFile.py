'''
Created on 24 Aug 2017

@author: Mathias Bucher
'''
from ctr.Log import Log
from collections import OrderedDict
import os

class ConfigFile(object):
    '''
    This class holds a config file with values. It is 
    thought to use it as a persistent memory of 
    configurations.
    '''


    def __init__(self, log, path):
        '''
        Constructor
        '''
        self.log = log
        self.path = path
        
        if not os.path.exists(self.path):
            f = open(self.path, "w")
            f.close()
        
        self.log.add(self.log.Info, __file__, "init" )
        
    def setValue(self, name, value):
        '''Adds a value to config file'''
        f = open(self.path, "r")
        oldText = f.read()
        f.close()
        
        config = self.getDict(oldText)
        config[name] = value
        newText = ""
        for key in config:
            newText += key + " = " + config[key] + "\n"
        
        f = open(self.path, "w")
        f.write(newText)
        f.close()
            
    def getValue(self, name):
        '''Returns a value from config file if available'''
        f = open(self.path, "r")
        text = f.read()
        f.close()
        
        config = self.getDict(text)
        
        if name in config:
            return config[name]
        else:
            self.log.add(self.log.Warning, __file__, name + " not found" )
            return None
    
    def getDict(self, text):
        '''Transforms the text into a dict. Each line 
        becomes an entry of the ordered dict. All characters before 
        ' = ' are taken as key and the rest of the line as
        value'''
        config = OrderedDict()
        textarray = text.split("\n")
        for l in textarray:
            splitted = l.split(" = ")
            if splitted.__len__() >= 2:
                config[splitted[0]] = splitted[1]                
            else:
                self.log.add(self.log.Warning, __file__, "invalid config" )
        return config