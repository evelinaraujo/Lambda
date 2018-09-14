import json
import boto3

ec2 = boto3.client('ec2')
idarray=[]
def shutdown(event, context):
    instances = ec2.describe_instances(
    Filters = [{
        'Name': 'instance-state-name',
        'Values': ['running']
    }])
    for instance in instances['Reservations']:
        for i in instance['Instances']:
            id = i['InstanceId']
            idarray.append(id)
    # print idarray
    for id in idarray:
        # print id
        try:
            shutdown = ec2.stop_instances(InstanceIds=[id])
            print ("Shutting down instance %s " % id)
        except Exception as e:
            print(e)
            print ("There are no instances to shut down")
