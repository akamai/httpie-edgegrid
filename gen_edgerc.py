# Simple script to generate credentials file based on
# Copy/paste of the "{OPEN} API Administration" output
# Usage: python gen_edgerc.py <section_name>
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

import sys
import re
import ConfigParser
from os.path import expanduser

# For the sample diagnostic tools application the section name is set to 
# diagnostic_tools. If you wish to use a different section name, call the  
# script with a new section name as the argument.
if len(sys.argv) > 1 and not re.search(sys.argv[1],'default'):
	section_name = sys.argv[1]
	section_name_pretty = sys.argv[1]
else:
	section_name = "----DEFAULT----"
	section_name_pretty = "default"

print "After authorizing your client in the {OPEN} API Administration tool,"
print "export the credentials and paste the contents of the export file below," 
print "followed by control-D."
print

print "This program will create a section named %s" % section_name_pretty
print
sys.stdout.write('>>> ')

# Slurp in config
text = sys.stdin.read()

# Parse the config data
home = expanduser("~")
fieldlist = text.split()
index = 0
fields = {}

while index < len(fieldlist):
	if (re.search(r':$', fieldlist[index])):
		fields[fieldlist[index]] = fieldlist[index + 1]
	index += 1

# Process the config data
Config = ConfigParser.ConfigParser()
filename = "%s/.edgerc" % home
open(filename, 'a+').close()
	

# First, if we have a 'default' section protect it here
with open (filename, "r+") as myfile:
 	data=myfile.read().replace('default','----DEFAULT----')
	myfile.close()
with open (filename, "w") as myfile:
	myfile.write(data)
	myfile.close()


Config.read(filename)
configfile = open(filename,'w')

if section_name in Config.sections():
	print "\n\nReplacing section: %s" % section_name_pretty
	Config.remove_section(section_name)
else:
	print "\n\nCreating section: %s" % section_name_pretty

Config.add_section(section_name)
Config.set(section_name,'client_secret',fields['Secret:'])
Config.set(section_name,'host',fields['URL:'].replace('https://',''))
Config.set(section_name,'access_token',fields['Tokens:'])
Config.set(section_name,'client_token',fields['token:'])
Config.set(section_name,'max-body',131072)
Config.write(configfile)

configfile.close()

with open (filename, "r") as myfile:
 	data=myfile.read().replace('----DEFAULT----','default')
	myfile.close()
with open (filename, "w") as myfile:
	myfile.write(data)
	myfile.close()
	
