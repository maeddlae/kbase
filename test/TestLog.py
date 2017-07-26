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
    log = 0
    capturedOutput = 0
    logfile = os.path.dirname(os.path.abspath(__file__)) + "\log.txt"

    def setUp(self):
        self.capturedOutput = StringIO.StringIO()
        sys.stdout = self.capturedOutput
        self.log = Log(self.logfile)
        pass


    def tearDown(self):
        sys.stdout = sys.__stdout__
        os.remove(self.logfile)
        pass


    def testConsole(self):
        '''Tests console output and header by adding two log entries'''
        self.log.log(Log.Error, "File1", "Line", "This is the text")
        self.log.log(Log.Error, "File2", "Line", "This is the text")         
        expected = "Severity\tFile            Line  Text\n"
        expected += "Error\t\tFile1           Line  This is the text              \n"
        expected += "Error\t\tFile2           Line  This is the text              \n"
        actual = self.capturedOutput.getvalue()
        
        self.assertEqual(expected, actual, "\n\nExpected:\n" + expected + "\n\nActual:\n" + actual)
    
    def testLogfile(self):
        '''Tests logfile output and header by adding two log entries'''
        self.log.log(Log.Warning, "File1", "Line", "This is the text")
        self.log.log(Log.Info, "File2", "Line", "This is the text")  
        
        # Overwrite current time for this test. 
        # Otherwise this test would not run stable
        time = datetime.datetime.now()
        self.log.now = time
        user = getpass.getuser()
        s = "LOGFILE\n"
        s += "Date: " + repr(time.day) + \
        "." + repr(time.month) + "." + repr(time.year) + "\n"
        s += "Time: " + repr(time.hour) + ":" + repr(time.minute) + \
        ":" + repr(time.second) + "\n"
        s += "User: " + user + "\n"
        s += "-----------------------------\n"
        s += "Severity\tFile            Line  Text\n"
        s += "Warning\t\tFile1           Line  This is the text              \n"
        s += "Info\t\tFile2           Line  This is the text              \n"
        
        f = open(self.logfile, 'r')
        actual = f.read()
        f.close()
        
        self.assertEqual(s, actual, "\n\nExpected:\n" + s + "\n\nActual:\n" + actual)

    def testLongStrings(self):
        '''Tests whether log shortend name and text correctly'''
        self.log.log(Log.Error, "Verylongsillyfilename", "Line", "This is the text which is much longer than allowed")      
        expected = "Severity\tFile            Line  Text\n"
        expected += "Error\t\tVerylongsillyfi Line  This is the text which is much\n"
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
    