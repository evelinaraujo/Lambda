#!/usr/bin/python

import boto3
import logging
from datetime import datetime, timedelta


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def describe_ec2(event, context):

    client = boto3.client('ec2')
    # variable for ec2 instance
    
    ec2_id = ['']
    
    # Describe the ec2 instance and grab the ebs volume
    for id in ec2_id:
        response = client.describe_instances()
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                #print(instance)
                
                #Grab volume from instance
                volumes=instance['BlockDeviceMappings']
                for volume in volumes:
                        volume=volume['Ebs']['VolumeId']
                        print("Volume ID for instance ID %s is %s " % (id, volume))
                        date = (datetime.now()).strftime("%F")
                        snapshot_name="{0}-{1}".format('evelin-test', date)
                        #Create snapshot from volume
                        
                        snapshot=client.create_snapshot(
                            Description = "Snapshot for " + id, 
                            VolumeId=volume,
                            TagSpecifications=[
                                {
                                    'ResourceType': "snapshot",
                                    'Tags': [
                                        {
                                            'Key': 'name',
                                            'Value': snapshot_name,
                                            'Key': 'application',
                                            'Value': 'core_infrastructure',
                                            'Key': 'department',
                                            'Value': 'infrastructures',
                                            'Key': 'division',
                                            'Value': 'technology',
                                            'Key': 'environment',
                                            'Value': 'development' ,
                                            'Key': 'role',
                                            'Value': 'backup'

                                        },
                                    ]
                                }
                            ]
                        )
                        logging.info("%s is being created :) " % snapshot_name)

#Make sure to adjust the timeout on the function. Default is 3 seconds, needs at least 10 seconds 