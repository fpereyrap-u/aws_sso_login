# issue_temporary_credentials.py

import configparser
import os
import sys

import boto3
import click


client_id='f0REPKyF4yD2297BZmpRoXVzLWVhc3QtMQ'
client_secret='eyJraWQiOiJrZXktMTU2NDAyODA5OSIsImFsZyI6IkhTMzg0In0.eyJzZXJpYWxpemVkIjoie1wiZXhwaXJlZFwiOmZhbHNlLFwiY2xpZW50SWRcIjp7XCJ2YWx1ZVwiOlwiZjBSRVBLeUY0eUQyMjk3QlptcFJvWFZ6TFdWaGMzUXRNUVwifSxcImNsaWVudE5hbWVcIjpcImZwbGFwdG9wXCIsXCJjbGllbnRUeXBlXCI6XCJQVUJMSUNcIixcInRlbXBsYXRlQXJuXCI6bnVsbCxcInRlbXBsYXRlQ29udGV4dFwiOm51bGwsXCJleHBpcmF0aW9uVGltZXN0YW1wXCI6MTU5NTY1NTI3Ni42NTAwMDAwMDAsXCJjcmVhdGVkVGltZXN0YW1wXCI6MTU4Nzg3OTI3Ni42NTAwMDAwMDAsXCJ1cGRhdGVkVGltZXN0YW1wXCI6MTU4Nzg3OTI3Ni42NTAwMDAwMDAsXCJjcmVhdGVkQnlcIjpudWxsLFwidXBkYXRlZEJ5XCI6bnVsbH0ifQ.eJHas4vm8fnID4xwwY7_jCMq3FjIm-AZoHC-HLnlB14iD9U0FOwbMR0OP-aKKV1F',
start_url='string'

grant_type=
device_code=

account_id='161142984839'
role_name='AdministratorAccess'
access_token=

token_client = boto3.client('sso-oidc')

response = token_client.start_device_authorization(
    clientId=client_id,
    clientSecret=client_secret,
    startUrl=start_url
)

response = token_client.create_token(
    clientId= client_id, #R
    clientSecret=client_secret, #R
    grantType='string', #R
    deviceCode='string',#R
    code='string',
    refreshToken='string',
    scope=[
        'string',
    ],
    redirectUri='string'
)

def get_credentials(*, account_id, role_name):
    iam_client = boto3.client("iam")
    client = boto3.client('sso')

    username = iam_client.get_user()["User"]["UserName"]

    role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"
    role_session_name = f"{username}@{role_name}.{account_id}"

    # resp = sts_client.assume_role(
    #     RoleArn=role_arn,
    #     RoleSessionName=role_session_name
    # )

    response = client.get_role_credentials(
        roleName=role_name,
        accountId=account_id,
        accessToken='string'
    )

    return response["Credentials"]


def update_credentials_file(*, profile_name, credentials):
    aws_dir = os.path.join(os.environ["HOME"], ".aws")

    credentials_path = os.path.join(aws_dir, "credentials")
    config = configparser.ConfigParser()
    config.read(credentials_path)

    if profile_name not in config.sections():
        config.add_section(profile_name)

    assert profile_name in config.sections()

    config[profile_name]["aws_access_key_id"] = credentials["AccessKeyId"]
    config[profile_name]["aws_secret_access_key"] = credentials["SecretAccessKey"]
    config[profile_name]["aws_session_token"] = credentials["SessionToken"]

    config.write(open(credentials_path, "w"), space_around_delimiters=False)


# @click.command()
# @click.option("--account_id", required=True)
# @click.option("--role_name", required=True)
# @click.option("--profile_name")
# def save_assumed_role_credentials(account_id, role_name, profile_name):
#     if profile_name is None:
#         profile_name = account_id

#     credentials = get_credentials(
#         account_id=account_id,
#         role_name=role_name
#     )

#     update_credentials_file(profile_name=profile_name, credentials=credentials)


# if __name__ == "__main__":
#     save_assumed_role_credentials()