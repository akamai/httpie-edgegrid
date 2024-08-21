This example creates your new API client credentials.

To run this example:

1. Open a Terminal or shell instance.

2. Copy the below http statement and paste it to the Terminal or shell instance.

3. Specify the section header of the set of credentials to use.

   The `--edgegrid-config` argument for the location of your `.edgerc` file is optional, as it defaults to `~/.edgerc`.

4. Press `Enter` to run the http statement.

   A successful call returns a new API client with its `credentialId`. Use this ID in both the update and delete examples.

For more information on the call used in this example, see https://techdocs.akamai.com/iam-api/reference/post-self-credentials.

```
$ http --auth-type=edgegrid -a default: POST :/identity-management/v3/api-clients/self/credentials
```
