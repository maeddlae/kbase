'''
Created on 24 Jul 2017

@author: Mathias Bucher
'''
from ctr.Log import Log
from model.Model import Model
from view.View import View


class Controller():
    dbPath = "D:\Mathias Bucher\Documents\others\Basteln\Python\kbase\data\data.db"

    def __init__(self):
        '''Constructor'''
        self.actions = {"menuGoClicked" : self.buttonGoAction }
        self.log = Log("log.txt")
        self.view = View(self.log, self.actions)
        self.model = Model(self.log, self.dbPath)
        
        self.log.add(self.log.Info, __file__, "init" )
        
    def run(self):        
        self.view.run()
        
    def buttonGoAction(self, keyword):
        self.log.add(self.log.Info, __file__, "search for : " + keyword)
        
        entry = self.model.getEntry(keyword)
        
        if entry != None:
            self.view.drawEntry(entry)
        else:
            self.view.drawSearch()
            
    def entryNameChangeAction(self, newName):
        # todo
        pass

    def entryDescriptionChangeAction(self, newDescription):
        pass

    def entryKeywordChangeAction(self, newKeywords):
        pass
        
        
app = Controller()
app.run()