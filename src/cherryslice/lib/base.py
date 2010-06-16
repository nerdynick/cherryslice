'''
Created on Jun 27, 2009

@author: Nick Verbeck
'''
from cherrypy import expose, response
from templating import render, getTemplate

class BaseController(object):
	def setHeader(self, name, value):
		response.headers[name] = value;