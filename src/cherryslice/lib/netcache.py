'''
Created on Jan 29, 2012

@author: nerdynick
'''
import socket
import urllib2
import cherryslice.lib.memCaching

#Support all versions of Python
try:
    from hashlib import md5 
except Exception, e:
    from md5 import md5

def getUrlAndCache(url, cacheTime=900):
    key = md5("NetCache_"+url).hexdigest()
    cache = cherryslice.lib.memCaching.getInstance()
    html = cache.get(key)
    if html is None:
        html = getUrl(url)
        cache.set(key, html, cacheTime)
        
    return html
    
def getUrl(url):
    try:
        js = urllib2.urlopen(url, timeout=3)
        html = js.read()
        js.close()
    except urllib2.URLError:
        html = None
    except socket.error:
        html = None
        
    return html
    