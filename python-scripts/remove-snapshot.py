#!/usr/bin/python

#Removes snapshots that are more than 7 days old from given ec2

from datetime import datetime, timedelta
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

tag_key='Name'
tag_value = 'PnmacInstance'
days = 7
def delete_snapshot(ec2, snapshot):
    client = boto3.client('ec2')
    response = client.describe_snapshots(
        Filters = [
            {
                'Name': 'tag:'+tag_key,
                'Values': [tag_value]
            }
        ]
    )
    week_ago_time = (datetime.utcnow() - timedelta(weeks=1)).strftime("%F")

    snapshotlist=response
    for snap in snapshotlist['Snapshots']:
        snapshot = snap['SnapshotId']
        time=(snap['StartTime']).strftime("%F")
        #print(snapshot)
        if time < week_ago_time:
            client.delete_snapshot(snapshotId = snapshot)
            print("Deleting %s" % snapshot)
            logging.info("%s has been deleted" % snapshot)
        else:
            print("Can't delete %s . Time created was %s It hasn't been %s days " % (snapshot,time,days))
            logging.info("Nothing to remove")
