#!/usr/bin/python

import boto3
import logging
from datetime import datetime, timedelta

# Describe the ec2 instance and grab the ebs volume
client = boto3.resource('ec2')
# variable for ec2 instance
ec2_id = ['']

for id in ec2_id:
    response = client.Describe_instances()
    for i in response["Instances"]
    print(instance)
    print(instance['root-device-nmaae'])
    print(instance['block-device-mapping.volume-id'])

# date=
# for id in ec2_id:
#     snapshot = "{0}-{1}".format(id, date)
