#!/usr/bin/python

# Script needs to run on a cloudwatch event that get triggered at 12 AM everyday
import logging
from datetime import datetime,timedelta
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('rds')

identifier_name=['production', 'demo', 'dev']

week_ago_time = (datetime.now() - timedelta(weeks=1)).strftime("%F")
today = datetime.now().strftime("%F")
print ("Week ago time = %s " % week_ago_time)

def describe_snapshots():
    print ("We only want to keep snapshots that are 7 days old and created today")
    for identifier in identifier_name:
        snapshots = client.describe_db_snapshots(DBInstanceIdentifier = identifier, SnapshotType = "manual")['DBSnapshots']
        for snapshot in snapshots:
            logging.info("Following snapshot is for %s database " % identifier)
            # print snapshot
            snapshotage = snapshot['SnapshotCreateTime'].strftime("%F")
            snapshotname = snapshot['DBSnapshotIdentifier']
            # print snapshotage
            if snapshotage < week_ago_time:
                try:
                    print ("This snapshot will be deleted '%s'. Snapshot time created is %s which is older than a week ago" % (snapshotname, snapshotage))
                    # uncomment the following line when ready to have script run
                    # client.delete_db_snapshot(DBSnapshotIdentifier = snapshotname)
                except Exception as e:
                    logging.error(e)
            if snapshotage == today and snapshotage > week_ago_time:
                try:
                    print ("Wont delete this snapshot since it was created today")
                except Exception as e:
                    logging.error(e)
            else:
                try:
                    print ("This snapshot will be deleted '%s'. Snapshot time created is %s which is less than a week old." % (snapshotname, snapshotage))
                    # uncomment the following line when ready to have script run
                    # client.delete_db_snapshot(DBSnapshotIdentifier = snapshotname)
                except Exception as e:
                    logging.error(e)

def main(event, context):
    describe_snapshots()

