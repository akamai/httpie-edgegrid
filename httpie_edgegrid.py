"""
edgegrid auth plugin for HTTPie.

"""
import sys
 
from httpie.plugins import AuthPlugin
<<<<<<< HEAD
from akamai.edgegrid import EdgeGridAuth
import ConfigParser, os
__version__ = '1.0.0'
__author__ = 'Kirsten Hunter'
__licence__ = 'Apache 2.0'

class MyEdgeGridAuth(EdgeGridAuth):


    def __call__(self, r):
        r = super(MyEdgeGridAuth, self).__call__(r)
        #r.headers['Host'] = os.environ['HOST'] 
	r.url = r.url.replace("http","https")
	r.url = r.url.replace("localhost/",os.environ['HOST'])
        return r


=======
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
 
 
>>>>>>> d95e001dbcc3cc03e548d95b654bc6e5858c9304
class EdgeGridPlugin(AuthPlugin):
 
    name = 'EdgeGrid auth'
    auth_type = 'edgegrid'
    description = ''
<<<<<<< HEAD

    def get_auth(self,username,password):
    	arguments = {}
    	config = ConfigParser.ConfigParser()
	home = os.environ['HOME']	
	print "signing"
    	config.readfp(open("%s/.edgerc" % home))
    	if not config.has_section(username):
                        err_msg = "ERROR: No section named %s was found in your .edgerc file\n" % (configuration, arguments["config_file"])
                        err_msg += "ERROR: Please generate credentials for the script functionality\n"
                        err_msg += "ERROR: and run 'python gen_edgerc.py %s' to generate the credential file\n" % configuration
                        sys.exit( err_msg )
    	for key, value in config.items(username):
		arguments[key] = value	
		if key == "host":
			os.environ['HOST'] = value
        return MyEdgeGridAuth(
            client_token=arguments["client_token"],
            client_secret=arguments["client_secret"],
            access_token=arguments["access_token"]
=======
 
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
>>>>>>> d95e001dbcc3cc03e548d95b654bc6e5858c9304
        )
        return auth
