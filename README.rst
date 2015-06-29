httpie-edgegrid
===========

EdgeGrid plugin for `HTTPie <https://github.com/jkbr/httpie>`_.


Installation
------------

.. code-block:: bash

    $ pip install httpie-edgegrid


Usage
-----

.. code-block:: bash


The .edgerc file needs to be created in your home directory and organized by <section> like this:

[default]
client_secret = xxxx
host = xxxx # Note, don't include the https:// here
access_token = xxxx
client_token = xxxx
max-body = xxxx

[papi]
client_secret = xxxx
host = xxxx # Note, don't include the https:// here
access_token = xxxx
client_token = xxxx
max-body = xxxx

Once you have the credentials set up, here is an example of what the call would look like:

% http --auth-type edgegrid  -a default: :/diagnostic-tools/v1/locations

The auth-type needs to be edgegrid.  The -a is the section from the config file, and the endpoint starts with a :.

The generic version is:

http --auth-type edgegrid  -a <section_name>: :/<endpoint>

