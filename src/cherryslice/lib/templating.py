'''
Created on Jun 25, 2009

@author: Nick Verbeck
'''
from mako.lookup import TemplateLookup
import os
from cherryslice.config import APP_PATH

lookupDirs = [os.path.join(APP_PATH, 'views'),
			  os.path.join(os.path.dirname(__file__), '..', 'apps')]

lookup = TemplateLookup(directories=lookupDirs,
					    module_directory=os.path.join(APP_PATH, 'cache', 'template'))


def getTemplate(template):
	"""
	Special Loader to allow for overriding of CherrySlice application views
	"""
	if template[:3] == 'app':
		templates = template.split('/', 1)
		app = templates[0][4:]
		template = "/"+ app +"/views/"+ templates[1]
	return lookup.get_template(str(template)+".html")
	
	
def render(template, **kargs):
	template = getTemplate(template)
	return template.render(**kargs)