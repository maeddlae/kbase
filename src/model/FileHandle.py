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
     
        
    def getStreamFromDictFiles(self, files):
        '''Returns a binary stream where each filename (=key of files dict) is 
        followed by its content (=value of files dict)'''
        barray = []
        for key, value in files.iteritems():
            if isinstance(key, unicode):
                key = key.encode("utf-8")
            barray.append(bytearray(key))
            barray.append(value)
        stream = self.insertSyncWords(barray)
        return stream
        
    def getDictFilesFromStream(self, stream):
        '''Returns the files in a dictionary, where key = filename 
        and value = content. This method expects a bytestream where 
        filename is followed by content, separated by sync words'''
        blist = self.removeSyncWords(stream)
        
        files = dict()
        for i, b in enumerate(blist):
            
            # even elements are keys (=filenames)
            if i%2 == 0:
                key = str(b)
                files[key] = bytearray()
                
            # odd elements are values (=file contents)
            else:
                key = str(blist[i-1])
                files[key] = b
        return files
    
    def getStreamFromFiles(self, files):
        '''Converts the files list into a bytestream, 
        which can be stored in a database. The stream 
        separates the files by sync word'''
        return self.insertSyncWords(files)
    
    def getFilesFromStream(self, stream):
        '''Converts the stream into files. The files 
        must be separated by sync words'''
        return self.removeSyncWords(stream)
        
    def insertSyncWords(self, bytestreams):
        '''Returns a single bytestream which contains 
        all the streams of bytestreams list. The streams 
        are separated by sync word'''
        stream = bytearray()
        for s in bytestreams:
            if isinstance(s, unicode):
                s = s.encode("utf-8")
            s = bytearray(s)
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
            