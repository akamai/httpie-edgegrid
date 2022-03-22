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

import sys
import os
import re
import argparse
from os.path import expanduser

if sys.version_info[0] >= 3:
    # python3
    from configparser import ConfigParser
else:
    # python2.7
    from ConfigParser import ConfigParser

# This script will create a configuration section with the name of the client in your
# ~/.edgerc credential store. Many of the sample applications use the a section 
# named 'default' for ease when running them during API Bootcamps.


def generate_edgerc(arguments, edgerc_file, enable_interruption):
    if arguments.cred_file:
        print("+++ Reading from EdgeGrid credentials file:", arguments.cred_file)
        with open(os.path.expanduser(arguments.cred_file), "r") as credFile:
            text = credFile.read()
            credFile.close()
    else:
        print("""After authorizing your client in the {OPEN} API Administration tool,
    export the credentials and paste the contents of the export file below, 
    followed by control-D.
    """)
        sys.stdout.write('>>>\n')
        text = sys.stdin.read()
        sys.stdout.write('<<<\n\n')

    # load the cred data
    fieldlist = text.split()
    index = 0
    fields = {}

    # Parse the cred data
    while index < len(fieldlist):
        if re.search(r':$', fieldlist[index]):
            fields[fieldlist[index]] = fieldlist[index + 1]
        index += 1

    # Determine the section name giving precedence to -s value
    if arguments.config_section:
        section_name = arguments.config_section
        section_name_pretty = arguments.config_section
    else:
        section_name = fields['Name:']
        section_name_pretty = fields['Name:']
        print("+++ Found client credentials with the name: %s" % section_name)

    # Fix up default sections
    if section_name.lower() == "default":
        section_name = "----DEFAULT----"
        section_name_pretty = "default"

    # Process the original .edgerc file
    orig_config = ConfigParser()

    # If this is a new file, create it
    if not os.path.isfile(edgerc_file):
        print("+++ Creating new credentials file: %s" % edgerc_file)
        open(edgerc_file, 'a+').close()
    else:
        print("+++ Found credentials file: %s" % edgerc_file)

    # Recommend default section name if not present
    orig_config.read(edgerc_file)
    if 'default' not in orig_config.sections() and enable_interruption:
        reply = str(input(
            '\nThe is no default section in ~/.edgerc, do you want to use these credentials as default? [y/n]: '
        )).lower().strip()
        print()
        if reply[0] == 'y':
            section_name = "----DEFAULT----"
            section_name_pretty = "default"

    if section_name_pretty in orig_config.sections():
        print(">>> Replacing section: %s" % section_name_pretty)
        replace_section = True
    else:
        print("+++ Creating section: %s" % section_name_pretty)
        replace_section = False

    if enable_interruption:
        # Make sure that this is ok ~ any key to continue
        try:
            input("\nPress Enter to continue or ctrl-c to exit.")
        except SyntaxError:
            pass

    # We need a line for the output to look nice
    print()

    # If we have a 'default' section hide it from ConfigParser
    with open(edgerc_file, "r+") as myfile:
        data = myfile.read().replace('default', '----DEFAULT----')
        myfile.close()
    with open(edgerc_file, "w") as myfile:
        myfile.write(data)
        myfile.close()

    # Open the ~/.edgerc file for writing
    config = ConfigParser()
    config.read(edgerc_file)
    configfile = open(edgerc_file, 'w')

    # Remove a section that is being replaced
    if replace_section:
        print("--- Removing section: %s" % section_name_pretty)
        config.remove_section(section_name)

    # Add the new section
    print("+++ Adding section: %s" % section_name_pretty)
    config.add_section(section_name)
    config.set(section_name, 'client_secret', fields['Secret:'])
    config.set(section_name, 'host', fields['URL:'].replace('https://', ''))
    config.set(section_name, 'access_token', fields['Tokens:'])
    config.set(section_name, 'client_token', fields['token:'])
    config.set(section_name, 'max-body', '131072')
    config.write(configfile)

    configfile.close()

    # Undo the ConfigParser work around
    with open(edgerc_file, "r") as myfile:
        data = myfile.read().replace('----DEFAULT----', 'default')
        myfile.close()
    with open(edgerc_file, "w") as myfile:
        myfile.write(data)
        myfile.close()

    print("\nDone. Please verify your credentials with the verify_creds.py script.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""After authorizing your client
in the {OPEN} API Administration tool, export the credentials and process
them with this script.""")
    parser.add_argument('--config_section', '-s', action='store',
                        help='create new config section with this section name.')
    parser.add_argument('--cred_file', '-f', action='store',
                        help='use the exported file from the OPEN API Administration tool.')
    args = parser.parse_args()

    print("""Akamai OPEN API EdgeGrid Credentials

This script will create a configuration section in the local ~/.edgerc credential file.
""")
    generate_edgerc(args, "%s/.edgerc" % expanduser("~"), True)
