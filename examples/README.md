# Examples

This directory contains executable CRUD examples for Akamai API using a httpie. API calls used in these examples are available to all users. But, if you find one of the write examples doesn't work for you, talk with your account's admin about your privilege level.

## Run

To run any of the files:

1. Open a Terminal or shell instance.
2. Copy the http statement from the .txt file and paste it to the Terminal or shell instance.

   - Specify the location of your `.edgerc` file. The default is set to the home directory.
   - Provide the section header for the set of credentials you'd like to use. The default is `default`.
   - For update and delete operations, replace the dummy `credentialId` with your valid `credentialId`.

3. Press `Enter` to run the http statement.

## Sample files

The example in each file contains a call to one of the Identity and Access Management (IAM) API endpoints. See the [IAM API reference](https://techdocs.akamai.com/iam-api/reference/api) doc for more information on each of the calls used.

| Operation | Method | Endpoint |
| --- | --- | --- |
| [List your API client credentials.](/examples/get-credentials.txt) | `GET` | `/identity-management/v3/api-clients/self/credentials`  |
| [Create new API client credentials.](/examples/create-credentials.txt) <br /> This is a *quick* client and grants you the default permissions associated with your account. | `POST` | `/identity-management/v3/api-clients/self/credentials` |
| [Update your credentials by ID.](/examples/update-credentials.txt) | `PUT` | `/identity-management/v3/api-clients/self/credentials/{credentialId}` |
| [Delete your credentials by ID.](/examples/delete-credentials.txt) | `DELETE` | `/identity-management/v3/api-clients/self/credentials/{credentialId}` |

Suggested chained call order:

1. Get credentials to see your base information.
2. Create a client to create a new set of credentials.
3. Update credentials to inactivate the newly created set from step 2.
4. Delete a client to delete the inactivated credentials.
5. Get credentials to verify if they're gone (the status will be `DELETED`).