#!/usr/bin/env python

from distutils.core import setup

setup(name='CherrySlice',
      version='0.1',
      description='CherryPy Extention Framework',
      author='Nick Verbeck',
      author_email='nerdynick@gmail.com',
      packages=['cherryslice',
                'cherryslice.lib',
                'cherryslice.apps',
                'cherryslice.helpers',
                'cherryslice.models'],
     )
