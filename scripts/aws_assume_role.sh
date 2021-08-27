STS_CRED=($(aws sts assume-role --role-arn arn:aws:iam::<acc_num>:role/<team>/<deployer_role> --role-session-name role_session --query 'Credentials.[SecretAccessKey, SessionToken, AccessKeyId]' --output text))

export AWS_SECRET_ACCESS_KEY="${STS_CRED[0]}"
export AWS_SESSION_TOKEN="${STS_CRED[1]}"
export AWS_ACCESS_KEY_ID="${STS_CRED[2]}"