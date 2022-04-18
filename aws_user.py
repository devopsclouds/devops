import boto3
iam=boto3.client('iam')  
response=iam.delete_user(UserName="Hanuma")
res=iam.delete_user(UserName="Hanu")
