# httpie-edgegrid

EdgeGrid plugin for [HTTPie](https://github.com/jkbr/httpie).

## Installation

To install from sources:

``` bash
$ python setup.py install
```

When using python 3 on Mac, replace python with python3:

``` bash
$ python3 setup.py install
```

If you have problems installing from sources, you could use pip:

``` bash
$ pip install httpie-edgegrid
```

## Running tests in virtual environment

To test in a [virtual
environment](https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments),
run:

``` bash
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
$ python -m unittest discover
```

## Usage

The EdgeGrid plugin relies on a .edgerc credentials file that needs to be created in your home directory and organized by \[section\] following the format below. Each \[section\] can contain a different credentials set allowing you to store all of your credentials in a single .edgerc file.

``` bash
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
```

Once you have the credentials set up, here is an example of what an Akamai OPEN API call would look like:

``` bash
% http --auth-type edgegrid -a <section_name>: :/<api_endpoint>
```

### Example

Making the diagnostic-tools API [locations]{.title-ref} call:

``` bash
% http --auth-type edgegrid -a default: :/diagnostic-tools/v2/ghost-locations/available
```

## Parameters

`--edgegrid-config`

    Path to `.edgerc` credentials file (optional, defaults to `~/.edgerc`)

## Environment variables

`RC_PATH`

    Path to `.edgerc` credentials file (optional, equivalent to the `--edgegrid-config` parameter)

## Troubleshooting

MacOS Sierra users have reported the error \"http: error: argument \--auth-type/-A: invalid choice: \'edgegrid\' (choose from \'basic\', \'digest\')\" after installation. Try installing using pip instead.

The error \"ImportError: 'pyOpenSSL' module missing required functionality. Try upgrading to v0.14 or newer\" requires you to install an updated version of \`pyOpenSSL\`:

``` bash
$ pip install --ignore-installed pyOpenSSL
```

Since v0.9.4 of httpie the Mac homebrew package is build with python3. If you get an error for \"ImportError: No module named cryptography\" then probably you installed httpie-edgegrid with python2.7 (unsupported). To explicitly install with python3 use:

``` bash
$ sudo python3 setup.py install
```

Or with pip3:

``` bash
$ sudo pip3 install httpie-edgegrid
```

## Advisories

Starting with HTTPie version 2.3.0 uploads are streamed, causing an issue posting JSON payloads as those don\'t include a content-length causing an error with the [Edgegrid authentication libraries](https://github.com/akamai/AkamaiOPEN-edgegrid-python). See [Issue #49](https://github.com/akamai/AkamaiOPEN-edgegrid-python/issues/49) for more details
