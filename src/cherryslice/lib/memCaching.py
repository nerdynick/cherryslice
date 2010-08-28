'''
Created on Aug 27, 2010

@author: nick
'''
import memcache
import cherrypy

def getInstance():
    return MemcachedCache()

class MemcachedCache(object):
    def __init__(self):
        self.mem = memcache.Client(str(cherrypy.request.app.config["memcached"]['servers']).split(','))
        
    def loads(self, key):
        return self.mem.get(key)
    get = loads
        
    def dumps(self, key, value, exp=21600):
        return self.mem.set(key, value, exp)
    set = dumps
    