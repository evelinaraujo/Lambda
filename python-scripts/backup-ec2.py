#!/usr/bin/python

import boto3
import logging
from datetime import datetime, timedelta


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def describe_ec2(event, context):
    # Describe the ec2 instance and grab the ebs volume
    client = boto3.client('ec2')
    # variable for ec2 instance
    ec2_id = ['i-05167199d5ca187dc']
    
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
                        snapshot_name="{0}-{1}".format('evelin-test', date)
                        snapshot=client.create_snapshot(
                            Description = "Snapshot for " + id, 
                            VolumeId=volume,
                            TagSpecifications=[
                                {
                                    'ResourceType': "snapshot",
                                    'Tags': [
                                        {
                                            'Key': 'Name',
                                            'Value': snapshot_name
                                        },
                                    ]
                                }
                            ]
                        )
                        logging.info(snapshot + "is being created :) ")
                        logging.error("Womp need to catch some errors")
