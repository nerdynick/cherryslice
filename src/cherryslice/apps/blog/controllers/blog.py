'''
Created on Mar 14, 2010

@author: nick
'''
from cherryslice.lib.base import expose, BaseController, render
from cherryslice.apps.blog.models import post
import cherrypy

class Blog(BaseController):
    def getBaseURL(self):
        if cherrypy.request.app.root is self:
            return '/'
        else:
            return '/blog/'
        
    @expose
    def index(self, page=0):
        posts = post.getPage(page, pageLength=cherrypy.request.app.config["app.blog"]['pageLength'])
        return render('app.blog/index', posts=posts, baseURL=self.getBaseURL())
    
    @expose
    def default(self, *args):
        pass
    
    @expose
    def tag(self, tag=None):
        pass
        