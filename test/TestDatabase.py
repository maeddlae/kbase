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
        
        # deltee db
        if os.path.exists(self.dbPath):
            os.remove(self.dbPath)

    def testAddNew(self):
        n = ModelEntry(self.log, "bikes")
        n.description = "These are bikes"
        n.keywords.append("Yamaha")
        n.keywords.append("Kawasaki")
        
        self.db.addEntry(n)
        
        rows = self.getAllRows(self.dbPath)
        self.assertTrue(self.containsEntry(rows, n),"Entry has not been added")
        pass
    
    def testAddExisting(self):
        #todo
        pass
            
    def getAllRows(self, db):
        con = sqlite3.connect(db)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM entries")
        rows = cur.fetchall()
        con.close()
        return rows
    
    def containsEntry(self, rows, entry):
        hasRow = False
        
        keywords = self.getKeywordString(entry.keywords)
        
        for row in rows:
            if (row["name"] == entry.name and 
                row["description"] == entry.description and
                row["keywords"] == keywords):
                hasRow = True
            
        return hasRow
                
    def getKeywordString(self, keywords):
        "Returns puts all elements of keywords into a string, separated by comma"
        s = ""
        first = True
        for k in keywords:
            if first:
                first = False
            else:
                s += ","
            s += k
                    
        return s
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()