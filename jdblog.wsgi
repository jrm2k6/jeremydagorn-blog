import os
import sys
import site

ALLDIRS = ['/home/jeremydagorn/.virtualenvs/env7/lib/python2.7/site-packages']
#site.addsitedir("/home/jeremydagorn/.virtualenvs/env7/lib/python2.7/site-packages")

# Remember original sys.path.
prev_sys_path = list(sys.path) 

# Add each new site-packages directory.
for directory in ALLDIRS:
  site.addsitedir(directory)

# Reorder sys.path so new directories at the front.
new_sys_path = [] 
for item in list(sys.path): 
    if item not in prev_sys_path: 
        new_sys_path.append(item) 
        sys.path.remove(item) 
sys.path[:0] = new_sys_path 

activate_this = '/home/jeremydagorn/.virtualenvs/env7/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

sys.path.append(os.path.dirname(__file__))
from base import app as application
application.debug = True
import pprint

class LoggingMiddleware:

    def __init__(self, application):
        self.__application = application

    def __call__(self, environ, start_response):
        errors = environ['wsgi.errors']
        pprint.pprint(('REQUEST', environ), stream=errors)

        def _start_response(status, headers, *args):
            pprint.pprint(('RESPONSE', status, headers), stream=errors)
            return start_response(status, headers, *args)

        return self.__application(environ, _start_response)

application = LoggingMiddleware(application)
