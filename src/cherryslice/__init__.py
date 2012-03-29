import os
import sys
import cherrypy
from cherryslice import config

APP_PATH = os.getcwd()

def setup(loc=None):
    global APP_PATH
    
    if loc is not None:
        #Setup App Path for CherrySlice Application Overrides
        APP_PATH = os.path.dirname(loc)
        
        #Setup Import Path lookup. This is for applications running in 
        #mod_wsgi that aren't installed into the standard install locs
        sys.path.append(os.path.dirname(loc))
    
    #Setup CherryPy Global Configurations
    cherrypy.config.update(config.globalConfig())
    
def newApp(rootController, rootLoc='/', configFile='app.conf'):
    app = cherrypy.tree.mount(rootController, rootLoc, config=config.commonAppConfig())
    
    appFile = os.path.join(APP_PATH, configFile)
    if os.path.exists(appFile):
        app.merge(appFile)
        
    return app

def launchStandalone(app, port=8080):
    cherrypy.config.update({'server.socket_port':port})
    cherrypy.engine.start()
    cherrypy.engine.block()
    
def launchWSGI(app):
    cherrypy.log._set_screen_handler(cherrypy.log.access_log, False)
    cherrypy.log._set_screen_handler(cherrypy.log.error_log, False)
    return app