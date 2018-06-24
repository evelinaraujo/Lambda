#!/usr/bin/python

import boto3
import logging
from datetime import datetime, timedelta


def describe_ec2(event, context):
    # Describe the ec2 instance and grab the ebs volume
    client = boto3.client('ec2')
    # variable for ec2 instance
    ec2_id = ['']
    
    for id in ec2_id:
        response = client.describe_instances()
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                #print(instance)
                volumes=instance['BlockDeviceMappings']
                for volume in volumes:
                        volume=volume['Ebs']['VolumeId']
                        print("Volume ID for instance ID %s is %s " % (id, volume))
                        date = (datetime.now()).strftime("%F")
                        client.create_snapshot(
                            Description = "Snapshot for " + id, 
                            VolumeId=volume,
                            TagSpecifications=[
                                {
                                    'ResourceType': "instance"
                                    'Tags': [
                                        'Key': 'Name',
                                        'Value': Name="{0}-{1}".format(id, date),
                                        ]
                                }
                                ]
                                )
