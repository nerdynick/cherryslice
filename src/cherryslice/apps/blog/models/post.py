'''
Created on Mar 14, 2010

@author: nick
'''
from couchdb.mapping import Document, TextField, DateTimeField, ListField
from datetime import datetime
from cherryslice.lib.database import couch
import sys

def getPage(page=0, pageLength=10):
    skip = page*pageLength
    posts = Post.view(couch.getDB('blog'), 'blog/blog_dates', limit=pageLength, skip=skip)
    return posts

class Post(Document):
    title = TextField()
    post = TextField()
    tags = ListField(TextField())
    posted = DateTimeField()
    link = TextField()