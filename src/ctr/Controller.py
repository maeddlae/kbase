'''
Created on 24 Jul 2017

@author: Mathias Bucher
'''
from ctr.Log import Log
from model.Model import Model
from view.View import View


class Controller():

    def __init__(self):
        '''Constructor'''
        self.log = Log("log.txt")
        self.view = View(self.log)
        self.model = Model()
        
        self.log.add(self.log.Info, __file__, "init" )
        
    def run(self):
        print("hello world")
        
        self.view.draw(None)


app = Controller()
app.run()