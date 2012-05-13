'''
Created on Dec 31, 2010

@author: nick
'''
import PySQLPool
import cherrypy

def getDB():
    conn = PySQLPool.getNewConnection(**cherrypy.tree.apps[''].config["mysql"])
    return conn
    
def getQuery(db=None):
    if db is None:
        db = getDB()
        
    query = PySQLPool.getNewQuery(connection=db)
    return query