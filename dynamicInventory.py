import boto3
from botocore.exceptions import ClientError
import sys

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
                        instanceList.append(instance["PublicIpAddress"])
    
    if len(instanceList) > 0:
        msg = "Totally %s EC2 machines to process in the aws region %s...!!!" % (len(instanceList), reg)
    else:
        msg = "No EC2 machines matching with the EC2 name %s in the aws region %s" % (value, reg)
    print(msg)
    print(instanceList)
    return instanceList

def writeToInventoryFile(instanceList):
    f = open("inventory.txt", "r")
    contents = f.readlines()
    f.close()

    dele = []
    for i in range(0,len(contents)):
        if "ansible_host=" in contents[i]:
            dele.append(contents[i])
    for val in dele:
        contents.remove(val)

    index = 1
    msg = "node{} ansible_host={} ansible_connection=ssh ansible_user=ec2-user ansible_ssh_private_key_file=/tmp/my-key-pair.pem ansible_ssh_common_args='-o StrictHostKeyChecking=no'\n"
    for ip in instanceList:
        data = msg.format(index, ip)
        contents.insert(index, data)
        index=index+1

    f = open("inventory.txt", "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()


instanceList = getInstanceIdByTagName('new-blue-green', 'ap-south-1')
writeToInventoryFile(instanceList)