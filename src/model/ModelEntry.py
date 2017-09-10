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
        self.tags = []
        self.images = []
        self.files = dict()
        
        self.log.add(self.log.Info, __file__, "init: " + name)
        
    def isSupportedImageFile(self, filename):
        '''Returns true if the file is a supported image file type'''
        if filename.lower().endswith((".bmp", ".eps", ".gif", ".icns", 
                                     ".im", ".jpeg", ".jpeg 2000", 
                                     ".msp", ".pcx", ".png", ".ppm",
                                     ".spider", ".tiff", ".webp",
                                     ".xbm", ".jpg")):
            return True
        else:
            return False
