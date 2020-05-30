import boto3
import json, webbrowser, socket

client = boto3.client('sso-oidc')
sso_client = boto3.client('sso')

def device_registration(client_name, client_type):
    try:
        response_client_registration = client.register_client(
            clientName= client_name,
            clientType= client_type,
        )
        return response_client_registration['clientId'], response_client_registration['clientSecret']
    except Exception as e:
        return e

def get_auth_device(id, secret, start_url='https://cloud-uala.awsapps.com/start#/'):
    try:
        response_device_authorization = client.start_device_authorization(
            clientId=id,
            clientSecret=secret,
            startUrl=start_url
        )
        return response_device_authorization['verificationUriComplete'], response_device_authorization['deviceCode'], response_device_authorization['userCode']
    except Exception as e:
        return e


def get_token(id, secret, device_code, user_code):
    try:
        response_token_creation = client.create_token(
            clientId= id,
            clientSecret= secret,
            grantType='urn:ietf:params:oauth:grant-type:device_code', #review
            deviceCode= device_code,
            code= user_code
        )
        return response_token_creation['accessToken']
    except Exception as e:
        return e

def get_list_accounts(token):
    try:
        response_list_accounts = sso_client.list_accounts(
            # nextToken='string',
            maxResults=123,
            accessToken=token
        )
        return response_list_accounts['accountList']
    except Exception as e:
        return e

def get_roles_account(token, accountid):
    try:
        response_account_roles = sso_client.list_account_roles(
            # nextToken='string',
            maxResults=123,
            accessToken=token,
            accountId=accountid
        )
        return response_account_roles['roleList']
    except Exception as e:
        return e


clientId, clientSecrets = device_registration(socket.gethostname(), 'public')
url, deviceCode, userCode = get_auth_device(clientId, clientSecrets)

try:
    webbrowser.open(url)
except:
    print("Please manual login: %s \n" % (url))

input("After login, press Enter to continue...")

token = get_token(clientId, clientSecrets, deviceCode, userCode)

accounts_list = get_list_accounts(token)

for account in accounts_list:
    account_id = account['accountId']
    account_name = account['accountName']
    print (account_name, get_roles_account(token, account_id))