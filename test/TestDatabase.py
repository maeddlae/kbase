'''
Created on 11 Aug 2017

@author: Mathias Bucher
'''
from ctr.Log import Log
import unittest
from mock import MagicMock
import sqlite3
import os
from model.Database import Database
from model.ModelEntry import ModelEntry


class TestDatabase(unittest.TestCase):
    dbPath = "testdb.db"
    notExistingDbPath = "notexistingdb.dh"

    def setUp(self):
        self.log = Log("testlog.txt")
        self.log.add = MagicMock()
    
        # delete db
        if os.path.exists(self.dbPath):
            os.remove(self.dbPath)
            
        # create test entries
        self.e = []
        self.e.append(ModelEntry(self.log,"buildings"))
        self.e[0].description = "This is a building"
        self.e[0].keywords = ["Louvre"]
        self.e.append(ModelEntry(self.log,"planes"))
        self.e[1].description = "These are planes"
        self.e[1].keywords = ["F16", "F35"]
        self.e.append(ModelEntry(self.log,"test1"))
        self.e[2].description = "blabla"
        self.e[2].keywords = ["bla"]
        self.e.append(ModelEntry(self.log,"nametest"))
        self.e[3].description = "blublu"
        self.e[3].keywords = ["blu"]
        self.e.append(ModelEntry(self.log,"desc1"))
        self.e[4].description = "df eblublufd"
        self.e[4].keywords = ["ble", "bli"]
        self.e.append(ModelEntry(self.log,"key1"))
        self.e[5].description = "aasdf"
        self.e[5].keywords = ["blo", "blidff", "lkj"]
        
        # create test database
        testdb = sqlite3.connect(self.dbPath)
        c = testdb.cursor()
        c.execute("CREATE TABLE entries (name text, description text, keywords text)")
        for entry in self.e:
            s = entry.getStringFromKeywords(entry.keywords)
            c.execute("INSERT INTO entries VALUES (?, ?, ?)", (entry.name, entry.description, s))
        
        testdb.commit()
        testdb.close()
        
        # create db object to be tested
        self.db = Database(self.log, self.dbPath)

    def tearDown(self):
        # kill Database object. This must be done to close the connection to the db
        del self.db
        
        # delete db
        if os.path.exists(self.dbPath):
            os.remove(self.dbPath)
            
    def testIfNoDatabaseExists(self):
        dbWithoutDatabase = Database(self.log, self.notExistingDbPath)
        
        n = ModelEntry(self.log, "planes")
        dbWithoutDatabase.addEntry(n)
        self.assertTrue(dbWithoutDatabase.hasEntry(n))
        
        if os.path.exists(self.notExistingDbPath):
            os.remove(self.notExistingDbPath)

    def testHasEntryPositive(self):
        '''Questioned entry exists'''
        self.assertTrue(self.db.hasEntry(self.e[1]))
        
    def testHasEntryNegative(self):
        '''Questioned entry does not exist'''
        n = ModelEntry(self.log, "bikes")
        self.assertFalse(self.db.hasEntry(n))
    
    def testAddNew(self):
        '''Adds a new entry which did not exist before'''
        n = ModelEntry(self.log, "bikes")
        n.description = "These are bikes"
        n.keywords.append("Yamaha")
        n.keywords.append("Kawasaki")
        
        self.db.addEntry(n)
        
        rows = self.getAllRows(self.dbPath)
        self.assertTrue(self.containsEntry(rows, n))
    
    def testAddExisting(self):
        '''Trys to add an existing entry'''
        n = ModelEntry(self.log, "buildings")
        self.db.addEntry(n)
        rows = self.getAllRows(self.dbPath)
        self.assertFalse(self.containsEntry(rows, n),"Entry has been added")
        
    def testGetEntriesByNamePositive(self):
        '''Tests if an existing entry will be found'''
        exp = []
        exp.append(self.e[0])
        act = self.db.getEntriesByName(exp[0].name)
        
        self.assertEqual(exp.__len__(), act.__len__())
        for e, a in zip(exp, act):
            self.assertEqual(e.name, a.name)
            self.assertEqual(e.description, a.description)
            self.assertSequenceEqual(e.keywords, a.keywords, str)

    def testGetEntriesByNameNegative(self):
        '''Tests if entry does not exist'''        
        act = self.db.getEntriesByName("bikes")        
        self.assertEqual(act.__len__(),0)

    def testGetEntriesByKeywordPositive(self):
        '''Tests if an existing entry will be found'''
        exp = []
        exp.append(self.e[1])
        act = self.db.getEntriesByKeyword("F35")
        
        self.assertEqual(exp.__len__(), act.__len__())
        for e, a in zip(exp, act):
            self.assertEqual(e.name, a.name)
            self.assertEqual(e.description, a.description)
            self.assertSequenceEqual(e.keywords, a.keywords, str)

    def testGetEntriesByKeywordNegative(self):
        '''Tests if an not existing entry will not be found'''        
        act = self.db.getEntriesByKeyword("F34")        
        self.assertEqual(act.__len__(),0)

    def testGetEntriesByDescriptionPositive(self):
        '''Tests if an existing entry will be found'''
        exp = []
        exp.append(self.e[1])
        act = self.db.getEntriesByDescription("These")
        
        self.assertEqual(exp.__len__(), act.__len__())
        for e, a in zip(exp, act):
            self.assertEqual(e.name, a.name)
            self.assertEqual(e.description, a.description)
            self.assertSequenceEqual(e.keywords, a.keywords, str)

    def testGetEntriesByDescriptionNegative(self):
        '''Tests if an not existing entry will not be found'''        
        act = self.db.getEntriesByKeyword("muha")        
        self.assertEqual(act.__len__(), 0)
        
    def testUpdateEntryIfExists(self):
        '''Trys to update an entries keywords and description'''
        # update description
        n = self.e[1]        
        n.description = "These are beautiful planes"
        self.db.updateEntry(n)
        rows = self.getAllRows(self.dbPath)
        self.assertTrue(self.containsEntry(rows, n))
        
        # update keywords
        n = self.e[1]        
        n.keywords.append("Boeing")
        n.keywords.append("F35")
        self.db.updateEntry(n)
        rows = self.getAllRows(self.dbPath)
        self.assertTrue(self.containsEntry(rows, n))
        
    def testUpdateEntryIfNotExists(self):
        '''Trys to update an entries keywords and description'''
        n = ModelEntry(self.log, "bikes")
        self.db.updateEntry(n)
        rows = self.getAllRows(self.dbPath)
        self.assertFalse(self.containsEntry(rows, n))
        
    def testUpdateNameIfExists(self):
        '''Trys to update an entries name'''
        e = self.e[1]        
        newName = "bridges"
        self.db.updateNameOfEntry(e, newName)
        rows = self.getAllRows(self.dbPath)
        e.name = newName
        self.assertTrue(self.containsEntry(rows, e))
        
    def testUpdateNameIfNotExists(self):
        '''Trys to update an entries name which does not exist'''
        n = ModelEntry(self.log, "bikes")
        self.db.updateNameOfEntry(n, "blabla")
        rows = self.getAllRows(self.dbPath)
        n.name = "blabla"
        self.assertFalse(self.containsEntry(rows, n))
        
    def testGetEntriesByNameMulti(self):
        '''Tests if multiple entries can be found by name'''
        exp = []
        exp.append(self.e[2])    
        exp.append(self.e[3])      
        act = self.db.getEntriesByName("test")
        
        self.assertEqual(exp.__len__(), act.__len__())
        for e, a in zip(exp, act):
            self.assertEqual(e.name, a.name)
            self.assertEqual(e.description, a.description)
            self.assertSequenceEqual(e.keywords, a.keywords, str)
            
    def testGetEntriesByDescriptionMulti(self):
        '''Tests if multiple entries can be found by description'''
        exp = []
        exp.append(self.e[3])    
        exp.append(self.e[4])      
        act = self.db.getEntriesByDescription("lubl")
        
        self.assertEqual(exp.__len__(), act.__len__())
        for e, a in zip(exp, act):
            self.assertEqual(e.name, a.name)
            self.assertEqual(e.description, a.description)
            self.assertSequenceEqual(e.keywords, a.keywords, str)
    
    def testGetEntriesByKeywordMulti(self):
        '''Tests if multiple entries can be found by keyword'''
        exp = []
        exp.append(self.e[4])    
        exp.append(self.e[5])      
        act = self.db.getEntriesByKeyword("bli")
        
        self.assertEqual(exp.__len__(), act.__len__())
        for e, a in zip(exp, act):
            self.assertEqual(e.name, a.name)
            self.assertEqual(e.description, a.description)
            self.assertSequenceEqual(e.keywords, a.keywords, str)
    
    def getAllRows(self, db):
        '''Returns all entries of the database'''
        con = sqlite3.connect(db)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM entries")
        rows = cur.fetchall()
        con.close()
        return rows
    
    def containsEntry(self, rows, entry):
        '''Checks if an entry exists in the rows. Method checks name, description and keywords'''
        hasRow = False
        
        keywords = entry.getStringFromKeywords(entry.keywords)
        
        for row in rows:
            if (row["name"] == entry.name and 
                row["description"] == entry.description and
                row["keywords"] == keywords):
                hasRow = True
            
        return hasRow   
    
    def testRemoveEntry(self):
        '''Checks if an entry is removed correctly'''
        # remove existing
        self.db.removeEntry(self.e[5])
        rows = self.getAllRows(self.dbPath)
        self.assertFalse(self.containsEntry(rows, self.e[5]))
        
        # remove not existing
        n = ModelEntry(self.log, "lkjh")
        self.db.removeEntry(n)
        rows = self.getAllRows(self.dbPath)
        self.assertTrue(self.containsEntry(rows, self.e[0]))
        self.assertTrue(self.containsEntry(rows, self.e[1]))
        self.assertTrue(self.containsEntry(rows, self.e[2]))
        self.assertTrue(self.containsEntry(rows, self.e[3]))
        self.assertTrue(self.containsEntry(rows, self.e[4]))
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()