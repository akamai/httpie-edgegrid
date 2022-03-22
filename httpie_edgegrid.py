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
        # Here we can decorate with Agent Header (or sth)
        r = super(HTTPieEdgeGridAuth, self).__call__(r)
        r.url = r.url.replace("http:", "https:")
        r.url = r.url.replace("localhost/", self.__hostname)
        return super(HTTPieEdgeGridAuth, self).__call__(r)


class EdgeGridPlugin(AuthPlugin):
    name = 'EdgeGrid auth'
    auth_type = 'edgegrid'
    description = ''
    edgerc_location = "~/.edgerc"

    def get_auth(self, username, password):
        rc_path = os.path.expanduser(self.edgerc_location)
        rc = EdgeRc(rc_path)

        if not rc.has_section(username):
            err_msg = "\nERROR: No section named '%s' was found in your .edgerc file\n" % username
            err_msg += "ERROR: Please generate credentials for the script functionality\n"
            err_msg += "ERROR: and run 'python gen_edgerc.py %s' to generate the credential file\n"
            sys.stderr.write(err_msg)
            sys.exit(1)

        host = rc.get(username, 'host')
        host = host.replace("https://", "")
        host = host.replace("/", "")
        host += "/"
        auth = HTTPieEdgeGridAuth(
            hostname=host,
            client_token=rc.get(username, 'client_token'),
            client_secret=rc.get(username, 'client_secret'),
            access_token=rc.get(username, 'access_token'),
            max_body=rc.getint(username, 'max_body')
        )
        return auth
