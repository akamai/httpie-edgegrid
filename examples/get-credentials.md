This example returns a list of your API client credentials.

To run this example:

1. Open a Terminal or shell instance.

2. Copy the below http statement and paste it to the Terminal or shell instance.

3. Specify the section header of the set of credentials to use.

   The `--edgegrid-config` argument for the location of your `.edgerc` file is optional, as it defaults to `~/.edgerc`.

4. Press `Enter` to run the http statement.

   A successful call returns your credentials grouped by `credentialId`.

For more information on the call used in this example, see https://techdocs.akamai.com/iam-api/reference/get-self-credentials.

```
$ http --auth-type=edgegrid -a default: :/identity-management/v3/api-clients/self/credentials
```
