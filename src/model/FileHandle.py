'''
Created on 31 Aug 2017

@author: Mathias Bucher
'''

class FileHandle(object):
    '''
    This class offers some methods for accessing files 
    in a sqlite database. It does not access the database 
    directly but offers methods to convert files into a 
    bytestream which can be stored in sql.
    '''
    syncword = bytearray([0xAA, 0xBB, 0xAA])
    syncwordshort = bytearray([0xAA, 0xBB])
    replaceword= bytearray([0xAA, 0xBB, 0xBB])

    def __init__(self, log):
        '''Constructor'''        
        self.log = log    
        self.log.add(self.log.Info, __file__, "init" )
     

    def getStreamFromFiles(self, files):
        '''Converts the files list into a bytestream, 
        which can be stored in a database. The stream 
        separates the files by sync word'''
        pass
    
    def getFilesFromStrean(self, stream):
        '''Converts the stream into files. The files 
        must be separated by sync words'''
        pass
        
    def insertSyncWords(self, bytestreams):
        '''Returns a single bytestream which contains 
        all the streams of bytestreams list. The streams 
        are separated by sync word'''
        stream = bytearray()
        for s in bytestreams:
            s = s.replace(self.syncwordshort, self.replaceword)
            stream.extend(s)
            stream.extend(self.syncword)
                
        return stream
    
    def removeSyncWords(self, stream):
        '''Removes the sync words of stream and returns 
        a list of the separated bytestreams'''
        splitted = stream.split(self.syncword)
        splitted = splitted[0:splitted.__len__()-1]
        bytestreams = []
        for s in splitted:
            s = s.replace(self.replaceword, self.syncwordshort)
            bytestreams.append(s)
        return bytestreams
            