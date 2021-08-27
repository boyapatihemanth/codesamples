import boto3
import os
import configparser

print("Enter OTP")
tokenCode = input().strip()

client = boto3.client('sts')

response = client.assume_role(
    RoleArn='arn:aws:iam::615547054056:role/deployer',
    RoleSessionName='deployerrole',
    SerialNumber="arn:aws:iam::589796708521:mfa/bh-localmacuser-deployer",
    TokenCode=tokenCode
)

# Print Response for debug purpose
#print(response)

aws_access_key_id = response['Credentials']['AccessKeyId']
aws_secret_access_key = response['Credentials']['SecretAccessKey']
aws_session_token = response['Credentials']['SessionToken']
print("Access Key: "+ aws_access_key_id)
print("Secret Access Key: "+ aws_secret_access_key)
print("Session Token: "+ aws_session_token)



config = configparser.ConfigParser()

HOME=os.environ["HOME"]
AWS_CONFIG_FILE = os.path.join(HOME, ".aws/credentials")
config.read(AWS_CONFIG_FILE)
#Print to debug if correct file is picked up or not
print(config.sections())
config['terraform']['aws_access_key_id'] = aws_access_key_id
config['terraform']['aws_secret_access_key'] = aws_secret_access_key
config['terraform']['aws_session_token'] = aws_session_token
with open(AWS_CONFIG_FILE, 'w') as configfile:
    config.write(configfile)
