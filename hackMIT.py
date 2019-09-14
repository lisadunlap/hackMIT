import boto3
from datetime import date, time, datetime, timezone
from check import fake_start, terminate_running, get_instance_info, get_all_running
from message import send_message

ec2client = boto3.client('ec2', region_name='us-east-2')
response = ec2client.describe_instances()
ec2 = boto3.resource('ec2', region_name='us-east-2')
#threshold_seconds = 1200

if __name__ == '__main__':
    threshold_seconds = input("What is the max length you want your instances to run(in minutes)? ")
    email = input("Enter your email so we can alert you of changes: ")
    stopped = get_all_running(int(threshold_seconds)*60)
    if stopped:
        send_message(email, threshold_seconds, stopped)