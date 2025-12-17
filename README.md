# EdgeGrid for HTTPie

EdgeGrid plugin for [HTTPie](https://github.com/jkbr/httpie).

This library implements an Authentication handler for HTTP requests using the [Akamai EdgeGrid Authentication](https://techdocs.akamai.com/developer/docs/authenticate-with-edgegrid) scheme for HTTPie.

## Install

To use the library, you need to have Python 3.9 or later installed on your system.

Then, install the `httpie-edgegrid` authentication handler from sources by running this command from the project root directory:

   ```
   pip install .
   ```

Alternatively, you can install it from PyPI (Python Package Index) by running:

```
pip install httpie-edgegrid
```

## Authentication

You can obtain the authentication credentials through an API client. Requests to the API are marked with a timestamp and a signature and are executed immediately.

1. [Create authentication credentials](https://techdocs.akamai.com/developer/docs/edgegrid).

2. Place your credentials in an EdgeGrid resource file, `.edgerc`, under a heading of `[default]` at your local home directory.

   ```
    [default]
    client_secret = C113nt53KR3TN6N90yVuAgICxIRwsObLi0E67/N8eRN=
    host = akab-h05tnam3wl42son7nktnlnnx-kbob3i3v.luna.akamaiapis.net
    access_token = akab-acc35t0k3nodujqunph3w7hzp7-gtm6ij
    client_token = akab-c113ntt0k3n4qtari252bfxxbsl-yvsdj
    ```

3. Use your local `.edgerc` by providing the path to your resource file and credentials' section header.

   The `--edgegrid-config` argument is optional, as it defaults to `~/.edgerc`.

    ```bash
    http --auth-type=edgegrid --edgegrid-config=<path/to/.edgerc> -a <credentials_section_name>: <METHOD> :/<api_endpoint>
    ```

   Alternatively, you can use an `RC_PATH` environment variable to point to the `.edgerc` resource file. It's equivalent to the `--edgegrid-config` argument.

   ```bash
   export RC_PATH=<path/to/.edgerc>
   ```

## Use

To use the library, provide your credentials section header and the appropriate endpoint information.

```bash
$ http --auth-type=edgegrid -a default: GET :/identity-management/v3/user-profile
```
> **Note:** You can omit the `METHOD` argument. If you don't specify it, HTTPie sets it by default to:
>
> - `GET` for requests without body
> - `POST` for requests with body

For details, see the [HTTPie documentation](https://httpie.io/docs/cli/optional-get-and-post).

### Query string parameter

When entering query parameters, pass them as name-value pairs separated with a double equal sign (`==`).

```bash
$ http --auth-type=edgegrid -a default: GET :/identity-management/v3/user-profile \
   authGrants==true \
   notifications==true \
   actions==true
```

For detail on adding query string parameters, see [HTTPie documentation](https://httpie.io/docs/cli/querystring-parameters).


### Headers

Enter request headers as name-value pairs separated with a colon (`:`).

> **Note:** You don't need to include the `Content-Type` and `Content-Length` headers. The authentication layer adds these values.

```bash
$ http --auth-type=edgegrid -a default: GET :/identity-management/v3/user-profile \
   Accept:application/json
```

For detail on setting headers, see [HTTPie documentation](https://httpie.io/docs/cli/http-headers).

### Body data

Use the [HTTPie syntax](https://httpie.io/docs/cli/non-string-json-fields) to pass simple JSON data in the request.

```bash
$ http --auth-type=edgegrid -a default: PUT :/identity-management/v3/user-profile/basic-info \
  contractType=Billing \
  country=USA \
  firstName=John \
  lastName=Smith \
  phone=3456788765 \
  preferredLanguage=English \
  sessionTimeOut:=30 \
  timeZone=GMT \
  Content-Type:application/json \
  Accept:application/json
```

To pass a nested JSON object, see [HTTPie documentation](https://httpie.io/docs/cli/nested-json) for details.

### Debug

Use the `--verbose` argument to enable debugging and get additional information on the HTTP request.

```
$ http --verbose --auth-type=edgegrid -a default: GET :/identity-management/v3/user-profile
```

In case of the HTTPie plugin's crash, add the `--traceback` argument to the request. It prints out the request's detailed stack trace. It's useful for [reporting issues](#reporting-issues).

## Run tests in virtual environment

The `venv` module is included in Python 3 by default.

To test in a [virtual environment](https://docs.python.org/3/library/venv.html):

1. Initialize your environment in a new directory.

   ```
   // Unix/macOS
   python3 -m venv ~/Desktop/myenv

   // Windows
   py -m venv ~/Desktop/myenv
   ```

   This creates a `venv` in the specified directory as well as copies pip into it.

2. Activate your environment.

   ```
   // Unix/macOS
   source ~/Desktop/myenv/bin/activate

   // Windows
   ~/Desktop/myenv/Scripts/activate
   ```

   Your prompt will change to show you're working in a virtual environment, for example:

   ```
   (myenv) jsmith@abc-de12fg $
   ```

3. To recreate the environment, install the required dependencies within your project.

   ```
   pip install -r dev-requirements.txt
   ```

4. Run the tests.

   ```
   // Unix/macOS
   pytest -v

   // Windows
   py -m pytest -v
   ```

5. To deactivate your environment, run the `deactivate` command.

## Troubleshooting

| Error message | Solution |
| ------- | -------|
| `http: error: argument --auth-type/-A: invalid choice: 'edgegrid' (choose from 'basic', 'digest')` | macOS Sierra users have reported this error after the package installation. To fix it, try installing the package using pip. |
| `ImportError: 'pyOpenSSL' module missing required functionality. Try upgrading to v0.14 or newer` | If you get this error, then you're required to install an updated version of `pyOpenSSL`: <br /> <br /> `$ pip install --ignore-installed pyOpenSSL`|
| `ImportError: No module named cryptography` | Starting with HTTPie v0.9.4, the Mac homebrew package is built with python3. If you get this error, then probably you've installed httpie-edgegrid with python2.7 (unsupported). To explicitly install with python3, run: <br /> <br /> `$ pip3 install .` <br /> <br /> Or: <br /> <br /> `$ pip3 install httpie-edgegrid` |

## Reporting issues

To report an issue or make a suggestion, create a new [GitHub issue](https://github.com/akamai/httpie-edgegrid/issues).

## License

Copyright 2026 Akamai Technologies, Inc. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use these files except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.