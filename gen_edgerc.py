#! /usr/bin/env python

# This script will generate a ~/.edgerc credentials file based on
# the output of the "{OPEN} API Administration" tool in Luna Control Center.
#
# Usage: python gen_edgerc.py -s <section_name> -f <export_file>

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

import sys, os
import re
import argparse
import ConfigParser
from os.path import expanduser

# This script will create a configuration section with the name of the client in your 
# ~/.edgerc credential store. Many of the sample applications use the a section 
# named 'default' for ease when running them during API Bootcamps.  

parser = argparse.ArgumentParser(description='After authorizing your client \
	in the {OPEN} API Administration tool, export the credentials and process \
	them with this script.')
parser.add_argument('--config_section', '-s', action='store', 
	help='create new config section with this section name.')
parser.add_argument('--cred_file', '-f', action='store', 
	help='use the exported file from the OPEN API Administration tool.')
args= parser.parse_args()

print "Akamai OPEN API EdgeGrid Credentials"
print
print "This script will create a configuration section in the local ~/.edgerc credential file."
print

if args.cred_file:
	print "+++ Reading from EdgeGrid credentials file:", args.cred_file
	with open (os.path.expanduser(args.cred_file), "r") as credFile:
			text = credFile.read()
			credFile.close()
else:
	print "After authorizing your client in the {OPEN} API Administration tool,"
	print "export the credentials and paste the contents of the export file below," 
	print "followed by control-D."
	print
	sys.stdout.write('>>>\n')
	text = sys.stdin.read()
	sys.stdout.write('<<<\n\n')

# load the cred data
home = expanduser("~")
fieldlist = text.split()
index = 0
fields = {}

# Parse the cred data
while index < len(fieldlist):
	if (re.search(r':$', fieldlist[index])):
		fields[fieldlist[index]] = fieldlist[index + 1]
	index += 1

# Determine the section name giving precedence to -s value
if args.config_section:
	section_name = args.config_section
	section_name_pretty = args.config_section
else:
	section_name = fields['Name:']
	section_name_pretty = fields['Name:']
	print "+++ Found client credentials with the name: %s" % section_name

# Fix up default sections
if section_name.lower() == "default":
	section_name = "----DEFAULT----"
	section_name_pretty = "default"

# Process the original .edgerc file
origConfig = ConfigParser.ConfigParser()
filename = "%s/.edgerc" % home

# If this is a new file, create it
if not os.path.isfile(filename):
	print "+++ Creating new credentials file: %s" % filename
	open(filename, 'a+').close()
else:
	print "+++ Found credentials file: %s" % filename
	
# Recommend default section name if not present
origConfig.read(filename)
if 'default' not in origConfig.sections():
	reply = str(raw_input('\nThe is no default section in ~/.edgerc, do you want to use these credentials as default? [y/n]: ')).lower().strip()
	print
	if reply[0] == 'y':
		section_name = "----DEFAULT----"
		section_name_pretty = "default"

if section_name_pretty in origConfig.sections():
	print ">>> Replacing section: %s" % section_name_pretty
	replace_section = True
else:
	print "+++ Creating section: %s" % section_name_pretty
	replace_section = False

# Make sure that this is ok ~ any key to continue
try:
	input("\nPress Enter to continue or ctrl-c to exit.")
except SyntaxError:
	pass

# We need a line for the output to look nice
print 

# If we have a 'default' section hide it from ConfigParser
with open (filename, "r+") as myfile:
 	data=myfile.read().replace('default','----DEFAULT----')
	myfile.close()
with open (filename, "w") as myfile:
	myfile.write(data)
	myfile.close()

# Open the ~/.edgerc file for writing
Config = ConfigParser.ConfigParser()
Config.read(filename)
configfile = open(filename,'w')

# Remove a section that is being replaced
if replace_section: 
	print "--- Removing section: %s" % section_name_pretty
	Config.remove_section(section_name)

# Add the new section
print "+++ Adding section: %s" % section_name_pretty
Config.add_section(section_name)
Config.set(section_name,'client_secret',fields['Secret:'])
Config.set(section_name,'host',fields['URL:'].replace('https://',''))
Config.set(section_name,'access_token',fields['Tokens:'])
Config.set(section_name,'client_token',fields['token:'])
Config.set(section_name,'max-body',131072)
Config.write(configfile)

configfile.close()

# Undo the ConfigParser work around
with open (filename, "r") as myfile:
	data=myfile.read().replace('----DEFAULT----','default')
	myfile.close()
with open (filename, "w") as myfile:
	myfile.write(data)
	myfile.close()

print "\nDone. Please verify your credentials with the verify_creds.py script."
print	
