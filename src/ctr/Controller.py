'''
Created on 24 Jul 2017

@author: Mathias Bucher
'''
from ctr.Log import Log


class Controller():
    log = 0

    def __init__(self):
        '''Constructor'''
        self.log = Log("log.txt")
        
        self.log.add(self.log.Info, __file__, "init" )
        
    def run(self):
        print("hello world")


app = Controller()
app.run()