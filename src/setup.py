#!/usr/bin/env python

from distutils.core import setup

setup(name='CherrySlice',
      version='0.1',
      description='CherryPy Extention Framework',
      author='Nick Verbeck',
      author_email='nerdynick@gmail.com',
      packages=['cherryslice',
                'cherryslice.lib',
                'cherryslice.lib.database',
                'cherryslice.apps',
                'cherryslice.apps.blog',
                'cherryslice.apps.blog.models',
                'cherryslice.apps.blog.controllers',
                'cherryslice.helpers',
                'cherryslice.models'],
      package_data={'cherryslice': ['apps/blog/views/index.html']}
     )
