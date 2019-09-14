import time
import boto3
import math
from datetime import date, time, datetime, timezone
from message import send_message

regions = ['us-west-1', 'us-west-2', 'us-east-1', 'us-east-2']

def fake_start(ec2client, ec2, dummy=True):
    response = ec2client.reboot_instances(
        InstanceIds=[
            'i-0a0e47a26e261db87',
        ],DryRun=dummy
    )
    return response

def terminate_running(info, ec2client, ec2):
    stopping = ec2client.stop_instances(InstanceIds=info["id"], DryRun=False)
    output = 'Stopping:'
    for n, i, l in zip(info["name"], info["id"], info['type']):
        output += " (Key Name: %s\t ID: %s\t Type: %s)\n"% (n, i, l)
    print(output)
    print("-------------------")

def get_instance_info(id, ec2client, ec2):
    response = ec2client.describe_instances(InstanceIds =[id])
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            # This sample print will output entire Dictionary object
            print(instance)
            # This will print will output the value of the Dictionary key 'InstanceId'
            print(instance["InstanceId"])

def get_running(threshold_seconds, ec2client, ec2, region):
    info = {"name":[], "id":[], "type":[]}
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    print("------------- Running Instances in %s --------------"% region)
    for i in instances:
        print("Key Name: %s\t Id: %s\t Type: %s"% (i.key_name, i.id, i.instance_type))
    print("----------------------------------")
    for instance in instances:
        time_run =datetime.now(timezone.utc)-instance.launch_time
        print("Instance %s has been running for %d minutes"% (instance.key_name, math.floor(time_run.seconds/60)))
        if time_run.seconds > threshold_seconds:
            print("Instance %s has been running to long..... Stopping now......."% (instance.key_name))
            info["name"] += [instance.key_name]
            info["id"] += [instance.id]
            info["type"] += [instance.instance_type]
        else:
            print("Instace %s still has %d minutes before auto-stopping"% (instance.key_name, math.floor(threshold_seconds - time_run.seconds)/60))
    if len(info['name']) > 0:
        terminate_running(info, ec2client, ec2)
        return info
    return None

def get_all_running(threshold_seconds):
    info = {"name":[], "id":[], "type":[]}
    for region in regions:
        ec2client = boto3.client('ec2', region_name=region)
        ec2 = boto3.resource('ec2', region_name=region)
        ret = get_running(threshold_seconds, ec2client, ec2, region)
        if ret:
            info["name"] += ret["name"]
            info["id"] += ret["id"]
            info["type"] += ret["type"]
    if len(info["name"]) > 0:
        return info
    return None