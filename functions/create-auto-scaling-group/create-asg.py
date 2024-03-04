import json
import boto3
import os
import base64

ec2_client = boto3.client('ec2')
client_asg = boto3.client('autoscaling')


def get_instance_id(event):
    # TODO implement
    try:
        response = ec2_client.describe_instance_types(
            DryRun=False,

            Filters=[
                {"Name": "memory-info.size-in-mib",
                 "Values": [event['config']["ram"], str(int(event['config']["ram"])+1)]},
                {"Name": "vcpu-info.default-vcpus",
                 "Values": [event['config']["cpu"], str(int(event['config']["cpu"])+1)]}
            ],
            MaxResults=100,
        )

        instance_id = ""
        for instance_ids in response['InstanceTypes']:
            print("In loops")
            print(instance_ids['ProcessorInfo']['SupportedArchitectures'][0])
            print(instance_ids['CurrentGeneration'])
            if str(instance_ids['CurrentGeneration']) == os.environ['bool']:
                print("In here")
                instance_id = instance_ids['InstanceType']
                cpu_arch = instance_ids['ProcessorInfo']['SupportedArchitectures'][0]
        print("0932khjdscjkhlsdcjhbcsjh")
        print(cpu_arch)
        if cpu_arch == "arm64":
            print("arm")
            ami_id = os.environ['AMI_ARM']
        else:
            print("x86")
            ami_id = os.environ['AMI_x86']
        print(instance_id)
        return [instance_id, ami_id]
    except Exception as err:
        print("In get")
        print(str(err))


def create_launch_template(event):
    # Define parameters
    userData = f"""#!/bin/bash
echo ECS_CLUSTER={event['data']["registry-name"]} >> /etc/ecs/ecs.config""".encode("us-ascii")
    template_name = event['data']["registry-name"]
    instance_info = get_instance_id(event)
    instance_type = "t3.micro"  # instance_info[0]
    image_id = "ami-0e5462b0cdd5ced35"  # instance_info[1]

    # Create Launch Template
    print("creating")
    response = ec2_client.create_launch_template(
        DryRun=False,
        LaunchTemplateName=template_name,
        VersionDescription="Model deploymetn",
        LaunchTemplateData={
            'EbsOptimized': False,
            'IamInstanceProfile': {
                'Arn': os.environ['ARN'],  # get from params
            },
            'BlockDeviceMappings': [
                {
                    'DeviceName': '/dev/xvda',
                    'Ebs': {
                        'VolumeSize': 120
                    }
                }
            ],
            'ImageId': image_id,
            'InstanceType': instance_type,
            'UserData': base64.b64encode(userData).decode('us-ascii')
        }
    )
    # Print the response
    print(response['LaunchTemplate']['LaunchTemplateName'])
    return response['LaunchTemplate']['LaunchTemplateName']


def create_asg(event):
    launch_template_name = create_launch_template(event)
    response = client_asg.create_auto_scaling_group(
        AutoScalingGroupName=event['data']["registry-name"],
        LaunchTemplate={
            "LaunchTemplateName": launch_template_name,
            "Version": "$Latest",  # Use the latest version of the Launch Template
        },
        MinSize=1,
        MaxSize=5,
        DesiredCapacity=1,
        VPCZoneIdentifier="subnet-046ece9627560a66a,subnet-030e86ba4defd393f,subnet-0b163826522f34c48",
        # ... other parameters (e.g., VPC ID, subnet IDs, security group IDs)
    )
    return 1


def lambda_handler(event, context):
    try:
        _ = create_asg(event)
    except Exception as er:
        print("in error")
        print(str(er))
    return {
        'statusCode': 200,
        'body': 1
    }
