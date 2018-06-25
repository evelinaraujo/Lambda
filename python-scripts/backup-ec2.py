#!/usr/bin/python


import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

tag_key = 'Name'
tag_value = 'PnmacInstance'
def describe_ec2(instance, snapshot):

    client = boto3.client('ec2')
    response = client.describe_instances(
        Filters=[
            {
                'Name' : 'tag:'+tag_key,
                'Values' : [tag_value]
            }
        ]
    )
    
    instancelist = response
    for i in instancelist:
        for reservation in instancelist['Reservations']:
            for instance in reservation['Instances']:
                id=instance["InstanceId"]
                print id
                
    #Grab volume from instance
    volumes = instance['BlockDeviceMappings']

    # for loop in case instance has more than one volume
    for volume in volumes:
        volume = volume['Ebs']['VolumeId']
        print("Volume ID for instance ID %s is %s " % (id, volume))
        
        #Create snapshot from volume
            
        client.create_snapshot(
            Description = "Snapshot for %s " % (tag_value), 
            VolumeId = volume,
            TagSpecifications = [
                {
                    'ResourceType': "snapshot",
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': tag_value,
                        },
                        {
                            'Key': 'application',
                            'Value': 'core_infrastructure'
                        },
                        {
                            'Key': 'department',
                            'Value': 'infrastructures'
                        },
                        {
                                'Key': 'division',
                            'Value': 'technology'
                        },
                        {
                            'Key': 'environment',
                            'Value': 'development'
                        },
                        {
                            'Key': 'role',
                            'Value': 'backup'

                        },
                    ]
                }
            ]
        )
        logging.info("%s is being created :) " % tag_value)

#Make sure to adjust the timeout on the function. Default is 3 seconds, needs at least 10 seconds 