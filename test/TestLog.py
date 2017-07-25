'''
Created on 25 Jul 2017

@author: Mathias Bucher
'''
import unittest
import StringIO
import sys
from ctr.Log import Log


class TestLog(unittest.TestCase):
    log = 0
    capturedOutput = 0

    def setUp(self):
        self.capturedOutput = StringIO.StringIO()
        sys.stdout = self.capturedOutput
        self.log = Log()
        pass


    def tearDown(self):
        sys.stdout = sys.__stdout__
        pass


    def testConsole(self):
        '''Tests console output and header by adding two log entries'''
        self.log.log(Log.Error, "File1", "Line", "This is the text")
        self.log.log(Log.Error, "File2", "Line", "This is the text")         
        expected = "Severity\tFile\tLine\tText\n"
        expected += "Error\tFile1\tLine\tThis is the text\n"
        expected += "Error\tFile2\tLine\tThis is the text\n"
        actual = self.capturedOutput.getvalue()
        
        self.assertEqual(
            expected,
            actual,
            "\n\nExpected:\n" + expected + "\n\nActual:\n" + actual)
        pass
