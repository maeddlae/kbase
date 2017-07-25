'''
Created on 24 Jul 2017

@author: Mathias Bucher
'''

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


    def __init__(self):
        '''
        Constructor
        '''
        print("Severity\tFile\tLine\tText") #print header
        
    def log(self, severity, name, line, text ):
        '''Adds an entry to the logfile and prints it to console'''
        s = self.severityToString(severity) + "\t" + name + "\t" + line + "\t" + text
        print(s)    #print log entry to console
    
    def severityToString(self, severity):
        '''Converts the severity into a string'''
        if severity == 0:
            return "Error"
        elif severity == 1:
            return "Warning"
        else:
            return "Info"