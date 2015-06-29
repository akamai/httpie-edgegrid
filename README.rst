httpie-edgegrid
===============

EdgeGrid plugin for `HTTPie <https://github.com/jkbr/httpie>`_.


Installation
------------

To install from sources:

.. code-block:: bash

    $ python setup.py install


Usage
-----

The EdgeGrid plugin relies on a .edgerc credentials file that needs to be created in your home directory and organized by [section] following the format below. Each [section] can contain a different credentials set allowing you to store all of your credentials in a single .edgerc file. 

.. code-block:: bash

		[default]
		client_secret = xxxx
		host = xxxx # Note, don't include the https:// here
		access_token = xxxx
		client_token = xxxx
		max-body = xxxx

		[section1]
		client_secret = xxxx
		host = xxxx # Note, don't include the https:// here
		access_token = xxxx
		client_token = xxxx
		max-body = xxxx

Once you have the credentials set up, here is an example of what an Akamai OPEN API call would look like:

.. code-block:: bash

	% http --auth-type edgegrid  -a <section_name>: :/<api_endpoint>

Set the auth-type to `edgegrid` and use -a `section_name:` to choose a credential set from the .edgerc credentials file. Start the api_endpoint with a `:` to avoid using the long Akamaia token based hostname.

Example
-------

Making the diagnostic-tools API `locations` call:

.. code-block:: bash

	% http --auth-type edgegrid  -a default: :/diagnostic-tools/v1/locations

