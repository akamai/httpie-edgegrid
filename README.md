# EdgeGrid for HTTPie

EdgeGrid plugin for [HTTPie](https://github.com/jkbr/httpie).

This library implements an Authentication handler for HTTP requests using the [Akamai EdgeGrid Authentication](https://techdocs.akamai.com/developer/docs/authenticate-with-edgegrid) scheme for HTTPie.

## Install

You can use pip, a standard package manager used to install and maintain packages for Python to install Edgrid for HTTPie. pip works on Linux, macOS, and Windows and always provides the latest version of HTTPie. pip is already installed on Python v3.6 or later. You can download the latest Python version from [python.org](https://www.python.org/downloads/).

Run this command to install the HTTPie authentication handler:

```
pip install httpie-edgegrid
```

## Authentication

We provide authentication credentials through an API client. Requests to the API are signed with a timestamp and are executed immediately.

1. [Create authentication credentials](https://techdocs.akamai.com/developer/docs/set-up-authentication-credentials).
   
2. Place your credentials in an EdgeGrid resource file, `.edgerc`, under a heading of `[default]` at your local home directory or the home directory of a web-server user.
   
   ```
    [default]
    client_secret = C113nt53KR3TN6N90yVuAgICxIRwsObLi0E67/N8eRN=
    host = akab-h05tnam3wl42son7nktnlnnx-kbob3i3v.luna.akamaiapis.net
    access_token = akab-acc35t0k3nodujqunph3w7hzp7-gtm6ij
    client_token = akab-c113ntt0k3n4qtari252bfxxbsl-yvsdj
    ```

3. Use your local `.edgerc` by providing the path to your resource file and credentials' section header.
   
   The `--edgegrid-config` argument is optional, as it  defaults to `~/.edgerc`.

    ```bash
    http --auth-type=edgegrid --edgegrid-config=<path/to/.edgerc> -a <credentials_section_name>: :/<api_endpoint>
    ```

## Use

To use the library, provide the path to your `.edgerc`, your credentials section header, and the appropriate endpoint information.

```bash
$ http GET --auth-type=edgegrid --edgegrid-config=~/.edgerc -a default: :/identity-management/v3/user-profile \
Accept: application/json'
```
> **Note:** The `METHOD` argument is optional, and when you don’t specify it, HTTPie defaults to:
> 
> - `GET` for requests without body
> - `POST` for requests with body

### Query string parameter

When entering query parameters, pass them as key-value pairs separated with a double equal sign (`==`).

```bash
$ http GET --auth-type=edgegrid --edgegrid-config=~/.edgerc -a default: :/identity-management/v3/user-profile \
authGrants==true \
notifications==true \
actions==true
```

### Headers

Enter request headers as key-value pairs separated with a colon (`:`).

> **Note:** You don't need to include the `Content-Type` and `Content-Length` headers. The authentication layer adds these values.

```bash
$ http GET --auth-type=edgegrid --edgegrid-config=~/.edgerc -a default: :/identity-management/v3/user-profile \
Accept: application/json
```

### Body data

You can use `printf` or `echo -n` to pipe simple data to the request.

```bash
$ printf '{
  "contactType": "Billing",
  "country": "USA",
  "firstName": "John",
  "lastName": "Smith",
  "phone": "3456788765",
  "preferredLanguage": "English",
  "sessionTimeOut": 30,
  "timeZone": "GMT",
}'| http PUT --auth-type=edgegrid --edgegrid-config=~/.edgerc -a default: :/identity-management/v3/user-profile/basic-info \
Content-Type: application/json \
Accept: application/json
```

To pass a nested JSON object, see [HTTPie documentation](https://httpie.io/docs/cli/nested-json) for details.

### Debug

Use the `--verbose` argument to enable debugging and get additional information on the HTTP request and response.

```
$ http --verbose GET --auth-type=edgegrid --edgegrid-config=~/.edgerc -a default: :/identity-management/v3/user-profile
```

## Run tests in virtual environment

To test in a [virtual
environment](https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments),
run:

1. Install the virtual environment.
   
   ```
   $ pip install virtualenv
   ```

2. Initialize your environment in a new directory.
   
   ```
   // Unix/macOS
   python3 -m venv ~/Desktop/myenv

   // Windows
   py -m venv ~/Desktop/myenv
   ```
   
   This creates a `venv` in the specified directory as well as copies pip into it.

3. Activate your environment.
   
   ```
   // Unix/macOS
   source ~/Desktop/myenv/bin/activate

   // Windows
   ~/Desktop/myenv/Scripts/activate
   ```

4. To recreate the environment, install the required dependencies within your project.
   
   ```
   pip install -r requirements_dev.txt
   ```

5. Initialize your tests.
   
   ```
   // Unix/macOS
   python -m unittest discover

   // Windows
   py -m unittest discover
   ```

## Troubleshooting

| Error message | Solution |
| ------- | -------|
| `http: error: argument --auth-type/-A: invalid choice: 'edgegrid' (choose from 'basic', 'digest')` | macOS Sierra users have reported this error after the package installation. To fix it, try installing the package using pip. |
| `ImportError: 'pyOpenSSL' module missing required functionality. Try upgrading to v0.14 or newer` | If you get this error, then you're required to install an updated version of `pyOpenSSL`: <br /> <br /> `$ pip install --ignore-installed pyOpenSSL`|
| `ImportError: No module named cryptography` | Starting with HTTPie v0.9.4, the Mac homebrew package is built with python3. If you get this error, then probably you've installed httpie-edgegrid with python2.7 (unsupported). To explicitly install with python3, run: <br /> <br /> `$ sudo python3 setup.py install` <br /> <br /> Or with pip3: <br /> <br /> `$ sudo pip3 install httpie-edgegrid` |

## Advisories

Starting with HTTPie v2.3.0, uploads are streamed, causing an issue with posting JSON payloads, as those don't include a content-length. As a result, there's an error with the [EdgeGrid authentication libraries](https://github.com/akamai/AkamaiOPEN-edgegrid-python). See [Issue #49](https://github.com/akamai/AkamaiOPEN-edgegrid-python/issues/49) for more details.

## Reporting issues

To report an issue or make a suggestion, create a new [GitHub issue](https://github.com/akamai/httpie-edgegrid/issues).

## License

Copyright 2023 Akamai Technologies, Inc. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.