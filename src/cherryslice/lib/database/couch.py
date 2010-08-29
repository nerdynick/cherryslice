'''
Created on Aug 28, 2010

@author: nick
'''
import couchdb
import cherrypy, sys

COUCH_DB = None
def getDB(db):
    global COUCH_DB
    db = str(cherrypy.request.app.config["couchdb"]['db_prepend'])+"_"+db
    if COUCH_DB is None:
        COUCH_DB = couchdb.client.Server(str(cherrypy.request.app.config["couchdb"]['server']))
        
    try:
        return COUCH_DB.create(db)
    except:
        return COUCH_DB[db]