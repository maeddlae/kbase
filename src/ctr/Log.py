'''
Created on 24 Jul 2017

@author: Mathias Bucher
'''

import os
import datetime
import getpass

class Log():
    '''
    This class writes log entries into a logfile and prints them to the console. 
    Entries are separated into three severities: Error, Warning and Info. You can 
    select the log severity of logfile and console separately. For example, if 
    CONSOLE_SEVERITY is set to Warning and LOGFILE_SEVERITY to Info, all 
    entries will be written to the logfile but only errors and warnings appear 
    in the console.
    '''
    Error, Warning, Info = range(3)
    CONSOLE_SEVERITY = Warning
    LOGFILE_SEVERITY = Info
    filepath = "log.txt"
    now = datetime.datetime.now()
    user = getpass.getuser()
    NAME_SIZE = 15
    TEXT_SIZE = 30


    def __init__(self, filepath):
        '''
        Constructor
        '''
        self.filepath = filepath
        
        # print header of console
        print(self.getRowHeader())

        # print header of logfile
        f = open(self.filepath,'w')
        f.write(self.getLogfileHeader())
        f.close()
        
    def add(self, severity, name, text ):
        '''Adds an entry to the logfile and prints it to console'''
        
        name = os.path.basename(name)
        name = self.resizeString(name, self.NAME_SIZE)
        text = self.resizeString(text, self.TEXT_SIZE)
        
        s = self.severityToString(severity) + "\t\t" + name + " "  + text
        print(s)    # print log entry to console
        self.writeToLogfile(s)   # write entry into logfile
    
    def severityToString(self, severity):
        '''Converts the severity into a string'''
        if severity == 0:
            return "Error"
        elif severity == 1:
            return "Warning"
        else:
            return "Info"
        
    def writeToLogfile(self, s):
        if os.path.exists(self.filepath):
            f = open(self.filepath,'a')
            f.write(s + "\n")
            f.close()
        
        
    def getRowHeader(self):
        return "Severity\tFile            Text"
        
    def getLogfileHeader(self):
        s = "LOGFILE\n"
        s += "Date: " + repr(self.now.day) + \
        "." + repr(self.now.month) + "." + repr(self.now.year) + "\n"
        s += "Time: " + repr(self.now.hour) + ":" + repr(self.now.minute) + \
        ":" + repr(self.now.second) + "\n"
        s += "User: " + self.user + "\n"
        s += "-----------------------------\n"
        s += self.getRowHeader() + "\n"
        return s
    
    def resizeString(self, s, n):
        if len(s) > n:
            s = s[0:n]
        else:
            numberOfSpaces = n - len(s)
            s += ' ' * numberOfSpaces
        return s
        