import boto3
import os
import configparser
import json
import click

HOME = os.environ["HOME"]
AWS_CONFIG_FILE = os.path.join(HOME, ".aws/credentials")
client = boto3.client('sts')

f = open('accounts.json',"r")
data = json.load(f)
f.close()

def get_environments():
    environments_list = []
    for environment in data:
        environments_list.append(environment)
    return environments_list


def get_available_roles():
    environments = get_environments()
    env_roles_didct = {}
    for environment in environments:
        roles_list = []
        for role in data[environment]:
            roles_list.append(role)
        env_roles_didct[environment] = roles_list
    return env_roles_didct

def assume_role(role_arn, role, tokenCode):
    try:
        response = client.assume_role(
            RoleArn=role_arn,
            RoleSessionName=role,
            SerialNumber="arn:aws:iam::589796708521:mfa/bh-localmacuser-deployer",
            TokenCode=tokenCode
        )

    except:
        print("Unable to Assume Role :" + role_arn + ". Issue can be because of many reasons, like no access, no role, OTP might be expired, etc.")
    else:
        aws_access_key_id = response['Credentials']['AccessKeyId']
        aws_secret_access_key = response['Credentials']['SecretAccessKey']
        aws_session_token = response['Credentials']['SessionToken']

        return aws_access_key_id, aws_secret_access_key, aws_session_token


def edit_credentials_file(aws_access_key_id,aws_secret_access_key, aws_session_token):
    config = configparser.ConfigParser()
    try:
        config.read(AWS_CONFIG_FILE)
    except:
        print("No credentials file  found at "+AWS_CONFIG_FILE+" Check file path")
    else:
        config['terraform']['aws_access_key_id'] = aws_access_key_id
        config['terraform']['aws_secret_access_key'] = aws_secret_access_key
        config['terraform']['aws_session_token'] = aws_session_token
        with open(AWS_CONFIG_FILE, 'w') as configfile:
            config.write(configfile)
        print("Config file edited")
        
@click.command()
@click.option('--environment', '-e', prompt='Environment', help='Accepts environment from: '+str(get_environments()))
@click.option('--role', '-r', prompt='Role', help='Accepts role from: '+str(get_available_roles()))
@click.option('--token_code', '-t', prompt='Token_code', help='Accepts MFA OTP')
def main(environment, role, token_code):
    account = data[environment][role]['account']
    role = data[environment][role]['role']
    arn_prefix = "arn:aws:iam::"
    role_prefix = ":role/"
    role_arn = arn_prefix + account + role_prefix + role
    print("Role to be Assumed is :" + role_arn)
    try:
        aws_access_key_id, aws_secret_access_key, aws_session_token = assume_role(role_arn, role, token_code)
    except:
        print("Assume Role failed")
    else:

        edit_credentials_file(aws_access_key_id, aws_secret_access_key, aws_session_token)

if __name__=="__main__":
    main()