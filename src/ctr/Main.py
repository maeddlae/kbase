'''
Created on 14 Aug 2017

@author: Mathias Bucher
'''

from ctr.Controller import Controller

class Main(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.ctr = Controller( None )
        
        
app = Main()
app.ctr.run()