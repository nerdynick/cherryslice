import os

def globalConfig(rootPath):
    return {
        'serve.socket_port': 8080,
        'server.thread_pool': 10,
        'tools.sessions.on': False,
        'tools.staticdir.root': os.path.abspath(rootPath)
    }

def appConfig():
    static = {
        'tools.staticdir.on': True,
        'tools.etags.on': True,
        'tools.etags.autotags': True,
        'tools.expires.on': True,
        'tools.expires.secs': 21600,
        'tools.expires.force': True,
        'tools.gzip.on': True
    }
    config = {
        '/css': dict(static),
        '/js': dict(static),
        '/images': dict(static),
        '/extra': dict(static)
    }
    config['/css'].update({'tools.staticdir.dir': 'static/css'})
    config['/js'].update({'tools.staticdir.dir': 'static/js'})
    config['/images'].update({'tools.staticdir.dir': 'static/images'})
    config['/extra'].update({'tools.staticdir.dir': 'static/extra'})
    
    return config