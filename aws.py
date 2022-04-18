import boto3
ec2 = boto3.resource('ec2')
ec3 = boto3.client('ec2')
  
instances= ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running','stopped']}])
print(instances)
for instance in instances:
    state=instance.state['Name']
    id=instance.id
    print(state)
    print(id)
	
	if state=="stopped":
        start=ec3.stop_instances(InstanceIds=id)
    elif state=="running":
        start=ec3.start_instances(InstanceIds=id)
    else:
        print("nothing")
	
