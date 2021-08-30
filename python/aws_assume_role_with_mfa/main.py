import boto3
import os
import configparser
import json

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

def get_available_roles(environment):
    roles_list = []
    for role in data[environment]:
        roles_list.append(role)
    return roles_list

def assume_role(role_arn, role, tokenCode):
    try:
        response = client.assume_role(
            RoleArn=role_arn,
            RoleSessionName=role,
            SerialNumber="arn:aws:iam::589796708521:mfa/bh-localmacuser-deployer",
            TokenCode=tokenCode
        )
        # Print Response for debug purpose
        #print(response)

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
        # Print to debug if correct credentials file is picked up or not
        # print(config.sections())
        config['terraform']['aws_access_key_id'] = aws_access_key_id
        config['terraform']['aws_secret_access_key'] = aws_secret_access_key
        config['terraform']['aws_session_token'] = aws_session_token
        with open(AWS_CONFIG_FILE, 'w') as configfile:
            config.write(configfile)
        print("Config file edited")



if __name__=="__main__":
    print("Enter Environment from below: ")
    print("Available Environments are:")
    environments_list = get_environments()
    print(environments_list)
    environment = input().strip()

    print("Enter Role: ")
    print("Available Roles for " +environment+ " are:")
    roles_list = get_available_roles(environment)
    print(roles_list)
    role = input().strip()
    # Need To work on validations of environment and role values entered

    account=data[environment][role]['account']
    role=data[environment][role]['role']
    arn_prefix = "arn:aws:iam::"
    role_prefix = ":role/"
    role_arn = arn_prefix+account+role_prefix+role
    print("Role to be Assumed is :"+role_arn)
    print("Enter OTP")
    tokenCode = input().strip()
    try:
        aws_access_key_id, aws_secret_access_key, aws_session_token = assume_role(role_arn, role, tokenCode)
    except:
        print("Assume Role failed")
    else:
        # BELOW ARE FOR DEBUGGING
        #print("Access Key: " + aws_access_key_id)
        #print("Secret Access Key: " + aws_secret_access_key)
        #print("Session Token: " + aws_session_token)

        edit_credentials_file(aws_access_key_id, aws_secret_access_key, aws_session_token)