# HTTPIE EDGEGRID RELEASE NOTES

## 2.1.4 (2024-06-06)

### Enhancements

* Updated `pyOpenSSL`, `pylint` and test dependencies

## 2.1.3 (2023-09-14)

### Enhancements

* Update `urllib3` and test dependencies

## 2.1.2 (2023-06-22)

### Bug fixes

* Fix bug returning unexpected error when performing basic API call ([I#34](https://github.com/akamai/httpie-edgegrid/issues/34))

### Enhancements

* Update `httpie` and `pyOpenSSL` dependencies

## 2.1.1 (2022-09-27)

### Enhancements

* Update edgegrid-python dependency

## 2.1.0 (2022-08-30)

### Enhancements

* Update edgegrid-python dependency

## 2.0.0 (2022-04-27)

### BREAKING CHANGES

* Dropped Python 2.7 support

### Enhancements

* New optional parameter: `--edgegrid-config`, the path for the `.edgerc` credentials file. It defaults to `~/.edgerc`
* New `RC_PATH` environment variable, equivalent to the `--edgegrid-config` parameter
