import boto3
from botocore.exceptions import ClientError
import sys
def getInstanceName(value,reg):
    #import boto3

    ec2 = boto3.client('ec2',region_name=reg)
    response = ec2.describe_instances()
    print(response)


def getInstanceIdByTagName(value, reg):
    filters = [{'Name':'tag:aws:cloudformation:stack-name','Values': ['%s' % (value)]}]
    msg = "Some Problem"
    ec2client = boto3.client('ec2', region_name=reg)
    instanceList = []
    response = ec2client.describe_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            for each_tag in instance.get("Tags"):
                if each_tag.get("Key") == "aws:cloudformation:stack-name" and each_tag.get("Value") == value:
                    if instance["State"]["Name"] == "running":
                        print(instance['PrivateIpAddress'])
                        instanceList.append(instance["PrivateIpAddress"])
    
    if len(instanceList) > 0:
        msg = "Totally %s EC2 machines to process in the aws region %s...!!!" % (len(instanceList), reg)
    else:
        msg = "No EC2 machines matching with the EC2 name %s in the aws region %s" % (value, reg)
    print(msg)
    print(instanceList)
    return instanceList



import boto3

client = boto3.client('autoscaling')
clientips=boto3.client('ec2')
paginator = client.get_paginator('describe_auto_scaling_groups')
page_iterator = paginator.paginate(
   PaginationConfig = {
      'PageSize': 100
   }
)

def lambda_handler(event, context):

   filtered_asgs = page_iterator.search(
      'AutoScalingGroups[] | [?contains(Tags[?Key==`{}`].Value, `{}`)]'.format('type', 'node')
   )

   for asg in filtered_asgs:
      print (asg['AutoScalingGroupName'])
      response = client.describe_auto_scaling_groups(
             AutoScalingGroupNames=[
        asg['AutoScalingGroupName'],
      ],
      )
      instances=response["AutoScalingGroups"][0]["Instances"]
      instanceids=[]
      for i in instances:
         instanceids.append(i["InstanceId"])
         instaneips=[]
         reservations = clientips.describe_instances(InstanceIds=[i['InstanceId']]).get("Reservations")
         for reservation in reservations:
            for instance in reservation['Instances']:
               print(instance.get("PublicIpAddress"))

instanceList = getInstanceIdByTagName('new-blue-green', 'ap-south-1')