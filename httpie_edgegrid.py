"""
edgegrid auth plugin for HTTPie.

"""
import sys
 
from httpie.plugins import AuthPlugin
from akamai.edgegrid import EdgeGridAuth, EdgeRc
import os 
 
__version__ = '1.0.0'
__author__ = 'Kirsten Hunter'
__licence__ = 'Apache 2.0'
 
 
class HTTPieEdgeGridAuth(EdgeGridAuth):
 
    def __init__(self, hostname, *args, **kwargs):
        self.__hostname = hostname
        super(HTTPieEdgeGridAuth, self).__init__(*args, **kwargs)
 
    def __call__(self, r):
        r = super(HTTPieEdgeGridAuth, self).__call__(r)
	r.url = r.url.replace("http","https")
	r.url = r.url.replace("localhost/",self.__hostname)
        return super(HTTPieEdgeGridAuth, self).__call__(r)
 
 
class EdgeGridPlugin(AuthPlugin):
 
    name = 'EdgeGrid auth'
    auth_type = 'edgegrid'
    description = ''
 
    def get_auth(self, username, password):
	home = os.environ['HOME']	
	rc = EdgeRc("%s/.edgerc" % home) 
 
        if not rc.has_section(username):
            err_msg = "\nERROR: No section named '%s' was found in your .edgerc file\n" % username
            err_msg += "ERROR: Please generate credentials for the script functionality\n"
            err_msg += "ERROR: and run 'python gen_edgerc.py %s' to generate the credential file\n"
            sys.stderr.write(err_msg)
            sys.exit(1)
 
        auth = HTTPieEdgeGridAuth(
            hostname=rc.get(username, 'host'),
            client_token=rc.get(username, 'client_token'),
            client_secret=rc.get(username, 'client_secret'),
            access_token=rc.get(username, 'access_token'),
            max_body=rc.getint(username, 'max_body')
        )
        return auth
