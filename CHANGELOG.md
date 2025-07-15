# RELEASE NOTES

## 2.2.2 (Jul 16, 2025)

### FEATURES/ENHANCEMENTS:

* Updated various dependencies.

## 2.2.1 (Apr 28, 2025)

### FEATURES/ENHANCEMENTS:

* Updated various dependencies.

### BUG FIXES:

* Removed unused dependencies.

## 2.2.0 (Dec 9, 2024)

### FEATURES/ENHANCEMENTS:

* Discontinued support for Python <= 3.8; Python 3.9 is now the minimum supported version.
* Updated several dependencies in `setup.py`.
* Started generating the `requirements.txt` and `dev-requirements.txt` files using `pip-compile`,
  so that they contain the full set of project dependencies.

### BUG FIXES:

* Fixed installation failure with HTTPie CLI ([I#76](https://github.com/akamai/httpie-edgegrid/issues/76)).

## 2.1.4 (Jun 6, 2024)

### FEATURES/ENHANCEMENTS:

* Updated the `pyOpenSSL`, `pylint`, and test dependencies.

## 2.1.3 (Sep 14, 2023)

### FEATURES/ENHANCEMENTS:

* Updated the `urllib3` and test dependencies.

## 2.1.2 (Jun 22, 2023)

### FEATURES/ENHANCEMENTS:

* Updated the `httpie` and `pyOpenSSL` dependencies.

### BUG FIXES:

* Fixed a bug related to returning an unexpected error when performing a basic API call ([I#34](https://github.com/akamai/httpie-edgegrid/issues/34)).

## 2.1.1 (Sep 27, 2022)

### FEATURES/ENHANCEMENTS:

* Updated the `edgegrid-python` dependency.

## 2.1.0 (Aug 30, 2022)

### FEATURES/ENHANCEMENTS:

* Updated the `edgegrid-python` dependency.

## 2.0.0 (Jul 22, 2022)

### BREAKING CHANGES:

* Dropped Python 2.7 support.

### FEATURES/ENHANCEMENTS:

* Added the new optional `--edgegrid-config` parameter for providing a path for the `.edgerc` credentials file. It defaults to `~/.edgerc`.
* Added the new `RC_PATH` environment variable, equivalent to the `--edgegrid-config` parameter.
