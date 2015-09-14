#! /usr/bin/env python

""" Copyright 2015 Akamai Technologies, Inc. All Rights Reserved.
 
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.

 You may obtain a copy of the License at 

    http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

#
# usage: verify_creds.py [-h] [--verbose] [--debug] 
#        [--config_file CONFIG_FILE] [--config_section CONFIG_SECTION]
#

import requests, logging, json, sys
from http_calls import EdgeGridHttpCaller
from akamai.edgegrid import EdgeGridAuth
from config import EdgeGridConfig
from urlparse import urljoin, urlparse

# Establish an HTTP session
session = requests.Session()

# Load the .edgerc credentials file
section_name = "default"
config = EdgeGridConfig({},section_name)

# Set up verbose output and debugging
if hasattr(config, "debug") and config.debug:
  debug = True
else:
	debug = False

if hasattr(config, "verbose") and config.verbose:
  verbose = True
else:
	verbose = False

# Set the EdgeGrid credentials
session.auth = EdgeGridAuth(
            client_token=config.client_token,
            client_secret=config.client_secret,
            access_token=config.access_token
)

# If include any special headers (used for debugging)
if hasattr(config, 'headers'):
  session.headers.update(config.headers)

# Set up the base URL
baseurl = '%s://%s/' % ('https', config.host)
httpCaller = EdgeGridHttpCaller(session, debug, verbose, baseurl)

# main code
if __name__ == "__main__":
	# Request the entitlement scope for the credentials
	credential_scope = httpCaller.getResult('/-/client-api/active-grants/implicit')

	if verbose: print json.dumps(credential_scope, indent=2)

	print "Credential Name: %s" % credential_scope['name']
	print "---"
	print "Created: %s by %s" % (credential_scope['created'], credential_scope['createdBy'])
	print "Updated: %s by %s" % (credential_scope['updated'], credential_scope['updatedBy'])
	print "Activated: %s by %s" % (credential_scope['activated'], credential_scope['activatedBy'])
	print "---"

	for scope in credential_scope['scope'].split(" "):
		o = urlparse(scope)
		apis = o.path.split("/")
		print '{0:35} {1:10}'.format(apis[3], apis[5])




