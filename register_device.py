import boto3
import json

client_name= 'fplaptop'
client_type= 'public'

client = boto3.client('sso-oidc')

response = client.register_client(
    clientName= client_name,
    clientType= client_type,
)

print (response)
print ('**************************')
jsonarray = json.dumps(response)

print (jsonarray)

with open('data.json', 'w') as f:
    json.dump(response, f)