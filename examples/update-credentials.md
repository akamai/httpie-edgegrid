This example updates the credentials from the create credentials example.

To run this example:

1. Open a Terminal or shell instance.

2. Copy the below http statement and paste it to the Terminal or shell instance.

3. Specify the section header of the set of credentials to use.

   The `--edgegrid-config` argument for the location of your `.edgerc` file is optional, as it defaults to `~/.edgerc`.

4. Add the `credentialId` for the set of credentials created using the create example as a path parameter.

5. Edit the `expiresOn` date to today's date. The date cannot be more than two years out or it will return a 400. Optionally, you can change the description value.

6. Press `Enter` to run the http statement.

   A successful call returns.

For more information on the call used in this example, see https://techdocs.akamai.com/iam-api/reference/put-self-credential.

 ```
$ http --auth-type=edgegrid -a default: PUT :/identity-management/v3/api-clients/self/credentials/123456 \
   description=Update-this-credential \
   expiresOn=2024-12-11T23:06:59.000Z \
   status=INACTIVE
   Accept:application/json \
   Content-Type:application/json
 ```