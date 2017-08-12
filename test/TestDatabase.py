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

    def setUp(self):
        self.log = Log("testlog.txt")
        self.log.add = MagicMock()
    
        # delete db
        if os.path.exists(self.dbPath):
            os.remove(self.dbPath)
            
        # create test database
        testdb = sqlite3.connect(self.dbPath)
        c = testdb.cursor()
        c.execute("CREATE TABLE entries (name text, description text, keywords text)")
        c.execute("INSERT INTO entries VALUES ('buildings', 'This is a building', 'Louvre')")
        c.execute("INSERT INTO entries VALUES ('planes', 'These are planes', 'F16,F35')")
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
            
    def testGetKeywordsFromString(self):
        exp = ["bla bla", "blu", " bleble", ""]
        inp = "bla bla,blu, bleble,"
        act = self.db.getKeywordsFromString(inp)
        self.assertSequenceEqual(exp,act,str)
            
    def testGetStringFromKeywords(self):
        exp = "asdf,sd swef ,a a, b b,"
        inp = ["asdf", "sd swef ", "a a", " b b", ""]
        act = self.db.getStringFromKeywords(inp)
        self.assertEqual(exp, act)

    def testHasEntryPositive(self):
        '''Questioned entry exists'''
        n = ModelEntry(self.log, "planes")
        self.assertTrue(self.db.hasEntry(n))
        
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
        
        keywords = self.db.getStringFromKeywords(entry.keywords)
        
        for row in rows:
            if (row["name"] == entry.name and 
                row["description"] == entry.description and
                row["keywords"] == keywords):
                hasRow = True
            
        return hasRow   

    def testGetEntryByNamePositive(self):
        '''Tests if an existing entry will be found'''
        exp = ModelEntry(self.log, "buildings")
        exp.description = "This is a building"
        exp.keywords.append("Louvre")
        
        act = self.db.getEntryByName(exp.name)
        
        self.assertEqual(exp.name, act.name)
        self.assertEqual(exp.description, act.description)
        self.assertSequenceEqual(exp.keywords, act.keywords, str)

    def testGetEntryByNameNegative(self):
        '''Tests if entry does not exist'''        
        act = self.db.getEntryByName("bikes")        
        self.assertEqual(act,None)

    def testGetEntryByKeywordPositive(self):
        '''Tests if an existing entry will be found'''
        exp = ModelEntry(self.log, "planes")
        exp.description = "These are planes"
        exp.keywords.append("F16")
        exp.keywords.append("F35")
        
        act = self.db.getEntryByKeyword("F35")
        
        self.assertEqual(exp.name, act.name)
        self.assertEqual(exp.description, act.description)
        self.assertSequenceEqual(exp.keywords, act.keywords, str)

    def testGetEntryByKeywordNegative(self):
        '''Tests if an not existing entry will not be found'''        
        act = self.db.getEntryByKeyword("F34")        
        self.assertEqual(act,None)

    def testGetEntryByDescriptionPositive(self):
        '''Tests if an existing entry will be found'''
        exp = ModelEntry(self.log, "planes")
        exp.description = "These are planes"
        exp.keywords.append("F16")
        exp.keywords.append("F35")
        
        act = self.db.getEntryByDescription("These")
        
        self.assertEqual(exp.name, act.name)
        self.assertEqual(exp.description, act.description)
        self.assertSequenceEqual(exp.keywords, act.keywords, str)

    def testGetEntryByDescriptionNegative(self):
        '''Tests if an not existing entry will not be found'''        
        act = self.db.getEntryByKeyword("muha")        
        self.assertEqual(act,None)
        
    def testUpdateEntryIfExists(self):
        '''Trys to update an entries keywords and description'''
        # update description
        n = ModelEntry(self.log, "planes")
        n.description = "These are beautiful planes"
        n.keywords.append("F16")
        n.keywords.append("F35")
        self.db.updateEntry(n)
        rows = self.getAllRows(self.dbPath)
        self.assertTrue(self.containsEntry(rows, n))
        
        # update keywords
        n = ModelEntry(self.log, "planes")
        n.description = "These are beautiful planes"
        n.keywords.append("Boeing")
        n.keywords.append("F35")
        self.db.updateEntry(n)
        rows = self.getAllRows(self.dbPath)
        self.assertTrue(self.containsEntry(rows, n))
        
    def testUpdateEntryIfNotExists(self):
        '''Trys to update an entries keywords and description'''
        
        # update description
        n = ModelEntry(self.log, "bikes")
        self.db.updateEntry(n)
        rows = self.getAllRows(self.dbPath)
        self.assertFalse(self.containsEntry(rows, n))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()