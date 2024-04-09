import json
import boto3
import os
import base64

ec2_client = boto3.client('ec2')
client_asg = boto3.client('autoscaling')



"""def get_instance_id(event):
    # TODO implement
    try:
        response = ec2_client.describe_instance_types(
            DryRun=False,
    
            Filters=[
                {"Name": "memory-info.size-in-mib",
                 "Values": [event['data']['ram'], str(int(event['data']['ram']))]},
                {"Name": "vcpu-info.default-vcpus",
                 "Values": [event['data']['cpu'], str(int(event['data']['cpu']))]}
            ],
            MaxResults=100,
        )
        print("in hereeeeeeee")
        print(response)
        instance_id=""
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
            ami_id=os.environ['AMI_ARM']
        else:
            print("x86")
            ami_id=os.environ['AMI_x86']
        print(instance_id)
        return [instance_id,ami_id]
    except Exception as err:
        print(str(err))
        vals = {"loc":["target_group","listner","task","ECS"]}
        raise ValueError(json.dumps(vals))
"""

def create_launch_template(event):
    try:
        # Define parameters
        userData=f"""#!/bin/bash
    
    echo ECS_CLUSTER={"mlops-"+event['data']["registry-name"]} >> /etc/ecs/ecs.config""".encode("us-ascii")
        template_name = "mlops-"+event['data']["registry-name"]
        #instance_info = get_instance_id(event)
        #instance_type = instance_info[0] #"t3.micro"
        #image_id = instance_info[1]  #"ami-0e5462b0cdd5ced35"
        instance_type = event['data']['instance_type']
        image_id = os.environ['AMI_ID']
        # Create Launch Template
        print("creating")
        response = ec2_client.create_launch_template(
            DryRun=False,
            LaunchTemplateName=template_name,
            VersionDescription="Model deployment",
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
                'UserData':base64.b64encode(userData).decode('us-ascii')
            }
        )
        # Print the response
        print(response['LaunchTemplate']['LaunchTemplateName'])
        return response['LaunchTemplate']['LaunchTemplateName']
    
    except Exception as err:
        print(str(err))
        vals = {"loc":["target_group","listner","task","ECS","launch_tmplate"],"registry":event['data']["registry-name"]}
        raise ValueError(json.dumps(vals))

def create_asg(event):
    try:
        launch_template_name = create_launch_template(event)
        response = client_asg.create_auto_scaling_group(
            AutoScalingGroupName="mlops-"+event['data']["registry-name"],
            LaunchTemplate={
                "LaunchTemplateName": launch_template_name,
                "Version": "$Latest",  # Use the latest version of the Launch Template
            },
            MinSize=1,
            MaxSize=5,
            DesiredCapacity=1,
            VPCZoneIdentifier=os.environ['SUBNETS'],
            # ... other parameters (e.g., VPC ID, subnet IDs, security group IDs)
        )
        
        print(response)
        return 1
        
    except Exception as err:
        vals = {"loc":["target_group","listner","task","ECS","launch_tmplate","asg"],"registry":event['data']["registry-name"]}
        raise ValueError(json.dumps(vals))

def lambda_handler(event, context):
    try:
        _ = create_asg(event)
    except Exception as er:
        print("in error")
        print(str(er))
    
    return event


