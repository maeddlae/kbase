'''
Created on 24 Jul 2017

@author: Mathias Bucher
'''
from ctr.Log import Log
from model.Model import Model
from model.ModelEntry import ModelEntry
from view.View import View
from model.ConfigFile import ConfigFile
import os


class Controller():
    configDataBase = "databasepath"
    
    def __init__(self, log, config):
        '''Constructor'''
        self.actions = {"searchAction" : self.searchAction,
                        "entryChangeAction" : self.entryChangeAction,
                        "newAction" : self.newEntryAction,
                        "showEntryAction" : self.entryClickedInVSearch,
                        "closedAction" : self.closeTabAction,
                        "tabChangeAction" : self.tabChangeAction,
                        "deleteAction" : self.deleteEntryAction,
                        "pathChangeAction" : self.changePathAction,
                        "newImageAction" : self.newImageAction,
                        "imageSelectedAction" : self.newImageSelectedAction,
                        "addTagAction" : self.newTagAction,
                        "deleteTagAction" : self.deleteTagAction,
                        "deleteImageAction" : self.deleteImageAction,
                        "deleteFileAction" : self.deleteFileAction,
                        "newFileAction" : self.newFileAction,
                        "fileSelectedAction" : self.newFileSelectedAction}
        if log != None:
            self.log = log
        else:
            self.log = Log("log.txt")
        
        self.config = ConfigFile( self.log, config )
        self.dbPath = self.config.getValue(self.configDataBase)
        self.view = View(self.log, self.dbPath, self.actions)
        self.model = Model(self.log, self.dbPath)
        self.isSearchActive = False
        
        self.log.add(self.log.Info, __file__, "init" )
        
    def run(self):        
        self.view.run()
        
    def searchAction(self, tag):
        self.log.add(self.log.Info, __file__, "search for : " + tag)
        results = self.model.getEntries(tag)
        self.view.drawSearch(results)
            
    def entryChangeAction(self, newName, newDescription):
        '''Simply calls update name from model with current entry'''
        self.view.removeEntry(self.model.currentEntry)
        self.model.updateNameOfEntry(self.model.currentEntry, newName)
        self.model.currentEntry.description = newDescription
        self.model.updateContentOfEntry(self.model.currentEntry)  
        self.model.currentEntry.name = newName
        self.view.drawEntry(self.model.currentEntry)

        
    def newEntryAction(self):
        '''Adds a new entry'''
        newNameText = "enter name"
        self.model.currentEntry = ModelEntry(self.log, newNameText)
        i = 0
        
        while self.model.hasEntry(self.model.currentEntry):
            i += 1
            newName = newNameText + str(i)
            self.model.currentEntry.name = newName
        
        self.model.openedEntries.append(self.model.currentEntry)
        self.model.addEntry(self.model.currentEntry)
        self.view.drawEntry(self.model.currentEntry)
        
    def entryClickedInVSearch(self, entryName):
        '''Shows the clicked entry'''     
        foundEntry = self.model.getFoundEntry(entryName)
        if foundEntry != None:
            self.model.currentEntry = foundEntry
            self.model.openedEntries.append(foundEntry)
            self.view.drawEntry(foundEntry)
            
        
    def closeTabAction(self):
        '''Closes the currently active tab'''
        if self.isSearchActive:
            self.view.removeSearch()
            self.model.currentEntry = None
        else:
            self.model.openedEntries.remove(self.model.currentEntry)
            self.view.removeEntry(self.model.currentEntry)
        
    def tabChangeAction(self, activeTabName, isSearchActive):
        '''Is called when tab focus changes'''
        # only do something when has a valid name
        if activeTabName != None:
            for e in self.model.openedEntries:
                if activeTabName == e.name:
                    self.model.currentEntry = e
                    self.view.setDeleteButton(True)
                    
        self.isSearchActive = isSearchActive
        if isSearchActive == True:
            self.view.setDeleteButton(False)
            
    def deleteEntryAction(self):
        '''Deletes the currently active entry'''
        self.model.removeEntry(self.model.currentEntry)
        self.view.removeEntry(self.model.currentEntry)
        
    def changePathAction(self, newPath):
        '''Changes the database path'''
        self.dbPath = newPath
        self.config.setValue(self.configDataBase, self.dbPath)
        self.model = Model(self.log, self.dbPath)
        self.view.changeDbPath(self.dbPath)
        
    def newImageAction(self):
        '''Is called when user wants to add a new image 
        by button click'''
        self.view.showNewImageSelectDialog()
        
    def newImageSelectedAction(self, filename):
        '''Is called when user has selected a new image. Method 
        adds the image to the model and shows it in view'''
        self.log.add(self.log.Info, __file__, "image " + filename + " selected")
        if os.path.exists(filename):
            f = open(filename, "rb")
            content = f.read()
            f.close()
            self.model.currentEntry.images.append(content)
            self.model.updateContentOfEntry(self.model.currentEntry)
            self.view.removeEntry(self.model.currentEntry)
            self.view.drawEntry(self.model.currentEntry)
            
    def deleteImageAction(self, imageToDelete):
        '''Deletes image number imageToDelete of current entry'''
        del self.model.currentEntry.images[imageToDelete]
        self.model.updateContentOfEntry(self.model.currentEntry)
        self.view.removeEntry(self.model.currentEntry)
        self.view.drawEntry(self.model.currentEntry)
            
    def newTagAction(self, newTag):
        '''This action is called when user entered a new tag'''
        self.model.currentEntry.tags.append(newTag)
        self.model.updateContentOfEntry(self.model.currentEntry)
        self.view.removeEntry(self.model.currentEntry)
        self.view.drawEntry(self.model.currentEntry)
        
    def deleteTagAction(self, tagToDelete):
        '''Is called when user deletes a tag'''
        self.model.currentEntry.tags.remove(tagToDelete)
        self.model.updateContentOfEntry(self.model.currentEntry)
        self.view.removeEntry(self.model.currentEntry)
        self.view.drawEntry(self.model.currentEntry)
        
    def newFileAction(self):
        '''Is called when user wants to add a new file 
        by button click'''
        self.view.showNewFileSelectDialog()
        
    def newFileSelectedAction(self, filename):
        '''Is called when user has selected a new file. Method 
        adds the file to the model and shows it in view'''
        self.log.add(self.log.Info, __file__, "file " + filename + " selected")
        if os.path.exists(filename):
            f = open(filename, "rb")
            content = f.read()
            f.close()
            name = os.path.basename(filename)
            self.model.currentEntry.files[name] = content
            self.model.updateContentOfEntry(self.model.currentEntry)
            self.view.removeEntry(self.model.currentEntry)
            self.view.drawEntry(self.model.currentEntry)
            
    def deleteFileAction(self, fileToDelete):
        '''Deletes file in current entry'''
        del self.model.currentEntry.files[fileToDelete]
        self.model.updateContentOfEntry(self.model.currentEntry)
        self.view.removeEntry(self.model.currentEntry)
        self.view.drawEntry(self.model.currentEntry)