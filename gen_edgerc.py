#! /usr/bin/env python

# This script will generate a ~/.edgerc credentials file based on
# the output of the "{OPEN} API Administration" tool in Luna Control Center.
#
# Usage: python gen_edgerc.py -s <section_name> -f <export_file>

import argparse
import os
import re
import sys
from configparser import ConfigParser
from os.path import expanduser


def generate_edgerc(arguments: argparse.Namespace,
                    edgerc_file: str,
                    enable_interruption: bool = True):
    """
    Creates a configuration section with the name of the client in your
    ~/.edgerc credential store. Many of the sample applications use the a section
    named 'default' for ease when running them during API Bootcamps.

    Args:
        arguments (argparse.Namespace): arguments parsed from the cmd
        edgerc_file (str): a path to '.edgerc'
        enable_interrupbion (bool): if True the script will interrupt with prompts (default=True)
    """
    fields = get_credentials_data(arguments.cred_file)

    # Determine the section name giving precedence to -s value
    if arguments.config_section:
        section_name = arguments.config_section
        section_name_pretty = arguments.config_section
    else:
        section_name = fields['Name:']
        section_name_pretty = fields['Name:']
        print(f"+++ Found client credentials with the name: {section_name}")

    # Fix up default sections
    if section_name.lower() == "default":
        section_name = "----DEFAULT----"
        section_name_pretty = "default"

    # Process the original .edgerc file
    orig_config = ConfigParser()

    # If this is a new file, create it
    if not os.path.isfile(edgerc_file):
        print(f"+++ Creating new credentials file: {edgerc_file}")
        with open(edgerc_file, 'a+'):
            pass
    else:
        print(f"+++ Found credentials file: {edgerc_file}")

    # Recommend default section name if not present
    orig_config.read(edgerc_file)
    if 'default' not in orig_config.sections() and enable_interruption:
        reply = str(input(
            f'\nThe is no default section in {edgerc_file}, ' +
            'do you want to use these credentials as default? [y/n]: '
        )).lower().strip()
        print()
        if reply[0] == 'y':
            section_name = "----DEFAULT----"
            section_name_pretty = "default"

    if section_name_pretty in orig_config.sections():
        print(f">>> Replacing section: {section_name_pretty}")
        replace_section = True
    else:
        print(f"+++ Creating section: {section_name_pretty}")
        replace_section = False

    if enable_interruption:
        # Make sure that this is ok ~ any key to continue
        try:
            input("\nPress Enter to continue or ctrl-c to exit.")
        except SyntaxError:
            pass

    # We need a line for the output to look nice
    print()

    add_section(edgerc_file, section_name,
                section_name_pretty, fields, replace_section)

    print("\nDone. Please verify your credentials with the verify_creds.py script.\n")


def get_credentials_data(cred_path: str) -> dict[str, str]:
    """
    Returns credentials data from provided file or input in a key-value format.

    Args:
        cred_path (str): a path to file with credentials

    Returns:
        dict[str, str]: key-value pairs found in the provided credentials
    """
    if cred_path:
        print("+++ Reading from EdgeGrid credentials file:", cred_path)
        with open(os.path.expanduser(cred_path), "r") as cred_file:
            text = cred_file.read()
    else:
        print("""After authorizing your client in the {OPEN} API Administration tool,
    export the credentials and paste the contents of the export file below, 
    followed by control-D.
    """)
        sys.stdout.write('>>>\n')
        text = sys.stdin.read()
        sys.stdout.write('<<<\n\n')

    return parse_credentials_data(text)


def parse_credentials_data(cred_text: str) -> dict[str, str]:
    """
    Finds key-value pairs in the passed data.

    Args:
        cred_text (str): content of credentials

    Returns:
        dict[str, str]: key-value pairs found in the provided credentials
    """
    fieldlist = cred_text.split()
    fields = {}

    for index, field in enumerate(fieldlist):
        if re.search(r':$', field):
            fields[field] = fieldlist[index + 1]

    return fields


def add_section(edgerc_file, section_name, section_name_pretty, fields, replace_section):
    """
    Adds a section in edgerc file.

    Args:
        edgerc_file (str)         - path to an edgerc file
        section_name (str)        - section name to be added/replaced
        section_name_pretty (str) - section name used in outputs
        fields (dict[str, str])   - credentials in key-value format
        replace_section (bool)    - True if section already exists and needs to be removed first
    """
    # If we have a 'default' section hide it from ConfigParser
    with open(edgerc_file, "r+") as myfile:
        data = myfile.read().replace('default', '----DEFAULT----')
    with open(edgerc_file, "w") as myfile:
        myfile.write(data)

    # Open the ~/.edgerc file for writing
    config = ConfigParser()
    config.read(edgerc_file)

    # Remove a section that is being replaced
    if replace_section:
        print(f"--- Removing section: {section_name_pretty}")
        config.remove_section(section_name)

    # Add the new section
    print(f"+++ Adding section: {section_name_pretty}")
    config.add_section(section_name)
    config.set(section_name, 'client_secret', fields['Secret:'])
    config.set(section_name, 'host', fields['URL:'].replace('https://', ''))
    config.set(section_name, 'access_token', fields['Tokens:'])
    config.set(section_name, 'client_token', fields['token:'])
    config.set(section_name, 'max-body', '131072')

    with open(edgerc_file, 'w') as configfile:
        config.write(configfile)

    # Undo the ConfigParser work around
    with open(edgerc_file, "r") as myfile:
        data = myfile.read().replace('----DEFAULT----', 'default')
    with open(edgerc_file, "w") as myfile:
        myfile.write(data)


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
    generate_edgerc(args, f'{expanduser("~")}/.edgerc')
