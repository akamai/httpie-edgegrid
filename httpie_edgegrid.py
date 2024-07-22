"""
 EdgeGrid auth plugin for HTTPie.

 Copyright 2024 Akamai Technologies, Inc. All Rights Reserved.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.

 You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
import argparse
import configparser
import os
import sys

from akamai.edgegrid import EdgeGridAuth, EdgeRc
from httpie.cli.definition import options, parser
from httpie.cli.options import ARGPARSE_QUALIFIER_MAP, Group, map_qualifiers
from httpie.plugins import AuthPlugin

__version__ = '1.0.6'
__licence__ = 'Apache 2.0'

RC_PATH = ''


def add_new_group(
        abstract_group: Group,
        concrete_parser: argparse.ArgumentParser
) -> None:
    """Add a new group to the existing parser"""
    concrete_group = concrete_parser.add_argument_group(
        title=abstract_group.name, description=abstract_group.description
    )
    if abstract_group.is_mutually_exclusive:
        concrete_group = concrete_group.add_mutually_exclusive_group(
            required=False)

    for abstract_argument in abstract_group.arguments:
        concrete_group.add_argument(
            *abstract_argument.aliases,
            **map_qualifiers(
                abstract_argument.configuration, ARGPARSE_QUALIFIER_MAP
            )
        )


class EdgeGridSetterAction(argparse.Action):
    """
    Action used to set RC_PATH variable
    """
    def __init__(self, #pylint: disable-msg=too-many-arguments
                 option_strings,
                 dest,
                 nargs=None,
                 const=None,
                 default=None,
                 type=None,
                 choices=None,
                 required=False,
                 help=None,
                 metavar=None):
        if nargs == 0:
            raise ValueError('nargs for store actions must be != 0; if you '
                             'have nothing to store, actions such as store '
                             'true or store const may be more appropriate')
        if const is not None and nargs != argparse.OPTIONAL:
            raise ValueError(
                f'nargs must be {argparse.OPTIONAL} to supply const')
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=nargs,
            const=const,
            default=default,
            type=type,
            choices=choices,
            required=required,
            help=help,
            metavar=metavar)

    def __call__(self, _, namespace, values, option_string=None):
        # Set the global RC_PATH
        global RC_PATH #pylint: disable-msg=global-statement
        RC_PATH = values


class HTTPieEdgeGridAuth(EdgeGridAuth):
    """
    A wrapper over the EdgeGridAuth
    """
    def __init__(self, hostname, *args, **kwargs):
        self.__hostname = hostname
        super().__init__(*args, **kwargs)

    def __call__(self, r):
        # Here we can decorate with Agent Header (or sth)
        r = super().__call__(r)
        r.url = r.url.replace("http:", "https:")
        r.url = r.url.replace("localhost/", self.__hostname)
        return super().__call__(r)


class EdgeGridPlugin(AuthPlugin): #pylint: disable-msg=too-few-public-methods
    """
    The EdgeGridPlugin builds HTTPieEdgeGridAuth based on the EdgeRC credentials
    """
    name = 'EdgeGrid auth'
    auth_type = 'edgegrid'
    description = ''

    def get_auth(self, username: str = None, password: str = None):
        rc_path = os.path.expanduser(
            RC_PATH or os.getenv("RC_PATH") or '~/.edgerc')

        if not os.path.exists(rc_path):
            err_msg = f"\nERROR: The provided {rc_path} file does not exist\n"
            err_msg += "ERROR: Please generate credentials for the script functionality\n"
            err_msg += "ERROR: and run 'python gen_edgerc.py %s' to generate the credential file\n"
            sys.stderr.write(err_msg)
            sys.exit(1)

        try:
            rc = EdgeRc(rc_path)
        except (configparser.DuplicateSectionError,
                configparser.MissingSectionHeaderError,
                UnicodeDecodeError):
            err_msg = f'''
ERROR: {rc_path} is not a valid .edgerc file
ERROR: Please generate credentials for the script functionality
ERROR: and run 'python gen_edgerc.py {rc_path}' to generate the credential file
'''
            sys.stderr.write(err_msg)
            sys.exit(2)

        if not rc.has_section(username):
            err_msg = f"\nERROR: No section named '{username}' was found in your .edgerc file\n"
            err_msg += "ERROR: Please generate credentials for the script functionality\n"
            err_msg += "ERROR: and run 'python gen_edgerc.py %s' to generate the credential file\n"
            sys.stderr.write(err_msg)
            sys.exit(3)

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


parser.register('action', 'edgerc', EdgeGridSetterAction)

edgegrid_group = options.add_group("EdgeGrid")
edgegrid_group.add_argument(
    '--edgegrid-config',
    action='edgerc',
    default='~/.edgerc',
    help='.edgerc credentials file (defaults to ~/.edgerc)'
)
edgegrid_group.finalize()
add_new_group(edgegrid_group, parser)
