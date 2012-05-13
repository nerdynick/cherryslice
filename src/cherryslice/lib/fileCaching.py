'''
Created on Jun 15, 2010

@author: nick
'''
import os
from cherryslice.config import APP_PATH
import stat
from datetime import datetime, timedelta
import pickle

class FileCache(object):
    def __init__(self, group, name):
        folder = os.path.join(APP_PATH, 'cache', group)
        try:
            os.makedirs(folder, 0777)
        except:
            pass
        self.filePath = os.path.join(folder, str(name)+'.cache')
        
    def loads(self, pickled=False, hours=6):
        if os.path.exists(self.filePath):
            mtime = datetime.fromtimestamp(os.stat(self.filePath)[stat.ST_MTIME])
            if datetime.now() - mtime >= timedelta(hours=hours):
                return None
        else:
            return None
        
        if pickled:
            return pickle.load(open(self.filePath, 'r'))
        else:
            return open(self.filePath, 'r').read()
        
    def dumps(self, string, pickled=False):
        if pickled:
            pickle.dump(string, open(self.filePath, 'w'))
        else:
            open(self.filePath, 'w').write(string)