'''
Created on 25 Jul 2017

@author: Mathias Bucher
'''
import unittest
import StringIO
import sys
import os
import datetime
import getpass
from ctr.Log import Log


class TestLog(unittest.TestCase):
    logfile = os.path.dirname(os.path.abspath(__file__)) + "\log.txt"

    def setUp(self):
        self.capturedOutput = StringIO.StringIO()
        sys.stdout = self.capturedOutput
        self.log = Log(self.logfile)
        pass


    def tearDown(self):
        sys.stdout = sys.__stdout__
        if os.path.exists(self.logfile):
            os.remove(self.logfile)
        pass
    
    def testIfWritesNotBeforeFirstAdd(self):
        '''Tests whether log is not printing to console and file before 
        add has been called'''
        expected = ""
        actual = self.capturedOutput.getvalue()
        self.assertEqual(expected, actual, "Log has already printed out:-(")

        # Logfile should be created at first call of add. So it should not 
        # exist here
        self.assertFalse(os.path.exists(self.logfile), "Logfile already exists")

    def testConsole(self):
        '''Tests console output and header by adding two log entries'''
        self.log.add(Log.Error, "File1", "This is the text")
        self.log.add(Log.Error, "File2", "This is the text")         
        expected = "Severity\tFile            Text\n"
        expected += "Error\t\tFile1           This is the text              \n"
        expected += "Error\t\tFile2           This is the text              \n"
        actual = self.capturedOutput.getvalue()
        
        self.assertEqual(expected, actual, "\n\nExpected:\n" + expected + "\n\nActual:\n" + actual)
    
    def testLogfile(self):
        '''Tests logfile output and header by adding two log entries'''
        time = datetime.datetime.now()
        self.log.now = time
        self.log.add(Log.Warning, "File1", "This is the text")
        self.log.add(Log.Info, "File2", "This is the text")  
        
        # Overwrite current time for this test. 
        # Otherwise this test would not run stable
        user = getpass.getuser()
        s = "LOGFILE\n"
        s += "Date: " + repr(time.day) + \
        "." + repr(time.month) + "." + repr(time.year) + "\n"
        s += "Time: " + repr(time.hour) + ":" + repr(time.minute) + \
        ":" + repr(time.second) + "\n"
        s += "User: " + user + "\n"
        s += "-----------------------------\n"
        s += "Severity\tFile            Text\n"
        s += "Warning\t\tFile1           This is the text              \n"
        s += "Info\t\tFile2           This is the text              \n"
        
        f = open(self.logfile, 'r')
        actual = f.read()
        f.close()
        
        self.assertEqual(s, actual, "\n\nExpected:\n" + s + "\n\nActual:\n" + actual)

    def testLongStrings(self):
        '''Tests whether log shortend name and text correctly'''
        self.log.add(Log.Error, "Verylongsillyfilename", "This is the text which is much longer than allowed")      
        expected = "Severity\tFile            Text\n"
        expected += "Error\t\tVerylongsillyfi This is the text which is much\n"
        actual = self.capturedOutput.getvalue()
        
        self.assertEqual(expected, actual, "\n\nExpected:\n" + expected + "\n\nActual:\n" + actual)
        
    def testResizeLongString(self):
        s = "abcdefgh"
        expected = "abcd"
        actual = self.log.resizeString(s, 4)
        self.assertEqual(expected, actual, "\n\nExpected:\n" + expected + "\n\nActual:\n" + actual)
    
    def testResizeShortString(self):
        s = "abc"
        expected = "abc  "
        actual = self.log.resizeString(s, 5)
        self.assertEqual(expected, actual, "\n\nExpected:\n" + expected + "\n\nActual:\n" + actual)
    