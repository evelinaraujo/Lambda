#!/usr/bin/python

from datetime import datetime
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
                'Values': [tag_value]
            }
        ]
    )
    
    instancelist = response
    for id in instancelist:
        for reservation in instancelist['Reservations']:
            for instance in reservation['Instances']:
                print(instance["InstanceId"])

    #Grab volume from instance
    volumes = instance['BlockDeviceMappings']

    # for loop in case instance has more than one volume
    for volume in volumes:
        volume = volume['Ebs']['VolumeId']
        print("Volume ID for instance ID %s is %s " % (id, volume))
        date = (datetime.now()).strftime("%F")
        snapshot_name = "{0}-{1}".format('evelin-test', date)
        
        #Create snapshot from volume
            
        client.create_snapshot(
            Description = "Snapshot for " + id, 
            VolumeId = volume,
            TagSpecifications = [
                {
                    'ResourceType': "snapshot",
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': snapshot_name,
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
        logging.info("%s is being created :) " % snapshot_name)

#Make sure to adjust the timeout on the function. Default is 3 seconds, needs at least 10 seconds 