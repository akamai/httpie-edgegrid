# Examples

This directory contains executable CRUD examples for Akamai API using a httpie. API calls used in these examples are available to all users. But, if you find one of the write examples doesn't work for you, talk with your account's admin about your privilege level.

## Run

To run any of the files:

1. Open a Terminal or shell instance.
2. Copy the http statement from the .txt file and paste it to the Terminal or shell instance.
   
   - Append the path to your `.edgerc`. The default is set to the home directory.
   - Provide the section header for the set of credentials you'd like to use. The default is `default`.
   
3. Press `Enter` to run the http statement.
    
## Sample files

The example in each file contains a call to one of the Identity and Access Management (IAM) API endpoints. See the [IAM API reference](https://techdocs.akamai.com/iam-api/reference/api) doc for more information on each of the calls used.

|Sample file|Endpoint|Description|
|---|---|---|
|[`get-credentials.txt`](/examples/get-credentials.txt)|`/identity-management/v3/api-clients/self/credentials`|Lists your API client credentials.|
|[`create-credentials.txt`](/examples/create-credentials.txt)|`/identity-management/v3/api-clients/self/credentials`|Creates a new API client. This is a *quick* client and grants you the default permissions associated with your account.|
|[`update-credentials.txt`](/examples/update-credentials.txt)|`/identity-management/v3/api-clients/self/credentials/{credentialId}`|Updates your credentials by ID.|
|[`delete-credentials.txt`](/examples/delete-credentials.txt)|`/identity-management/v3/api-clients/self/credentials/{credentialId}`|Deletes your credentials by ID.|

Suggested chained call order:

1. Get credentials to see your base information.
2. Create a client to create a new set of credentials.
3. Update credentials to inactivate the newly created set from step 2.
4. Delete a client to delete the inactivated credentials.
5. Get credentials to verify if they're gone (the status will be `DELETED`).