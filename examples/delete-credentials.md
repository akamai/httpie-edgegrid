This example deletes your API client credentials.

To run this example:

1. Open a Terminal or shell instance.

2. Copy the below http statement and paste it to the Terminal or shell instance.

3. Specify the section header of the set of credentials to use.

   The `--edgegrid-config` argument for the location of your `.edgerc` file is optional, as it defaults to `~/.edgerc`.

4. Add the `credentialId` from the update example to the path. You can only delete inactive credentials. Sending the request on an active set will return a 400. Use the update credentials example for deactivation.

5. Press `Enter` to run the http statement.

   A successful call returns "" null.

For more information on the call used in this example, see https://techdocs.akamai.com/iam-api/reference/delete-self-credential.

```
$ http --auth-type=edgegrid -a default: DELETE :/identity-management/v3/api-clients/self/credentials/123456
```
