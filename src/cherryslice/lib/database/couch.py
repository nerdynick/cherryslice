'''
Created on Aug 28, 2010

@author: nick
'''
import couchdb
import cherrypy

COUCH_DB = None
def getDB(db):
    global COUCH_DB
    db = str(cherrypy.tree.apps[''].config["couchdb"]['db_prepend'])+"_"+db
    if COUCH_DB is None:
        COUCH_DB = couchdb.client.Server(str(cherrypy.tree.apps[''].config["couchdb"]['server']))
        
    try:
        return COUCH_DB.create(db)
    except:
        return COUCH_DB[db]