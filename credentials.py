import boto3

client = boto3.client('sso')

response = client.get_role_credentials(
    roleName='string',
    accountId='string',
    accessToken='string'
)

return response["Credentials"]