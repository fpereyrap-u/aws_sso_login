import boto3
import json, webbrowser

client_name= 'fplaptop'
client_type= 'public'
start_url= 'https://cloud-uala.awsapps.com/start#/'

client = boto3.client('sso-oidc')

response_client_registration = client.register_client(
    clientName= client_name,
    clientType= client_type,
)

# print (response_client_registration)
# print ('**************************')
# jsonarray = json.dumps(response_client_registration)

# print (jsonarray)

# with open('data.json', 'w') as f:
#     json.dump(response_client_registration, f)

response_device_authorization = client.start_device_authorization(
    clientId= response_client_registration['clientId'],
    clientSecret= response_client_registration['clientSecret'],
    startUrl= start_url
)

url = response_device_authorization['verificationUriComplete']

webbrowser.open_new(url)
print ("Please manual login: %s \n" % (url))

input("After login, press Enter to continue...")


try:
    response_token_creation = client.create_token(
        clientId= response_client_registration['clientId'],
        clientSecret= response_client_registration['clientSecret'],
        grantType='urn:ietf:params:oauth:grant-type:device_code', #review
        deviceCode= response_device_authorization['deviceCode'],
        code=response_device_authorization['userCode'],
        #refreshToken='string',
    )
    print (response_token_creation)
except Exception as e:
    print (e)