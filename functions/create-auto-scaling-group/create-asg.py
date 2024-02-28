import json
import boto3
import os
ec2_client = boto3.client('ec2')
client_asg = boto3.client('autoscaling')


def get_instance_id(event):
    # TODO implement
    response = ec2_client.describe_instance_types(
        DryRun=False,

        Filters=[
            {"Name": "memory-info.size-in-mib",
             "Values": [event["memory"], str(int(event["memory"])+1)]},
            {"Name": "vcpu-info.default-vcpus",
             "Values": [event["cpu"], str(int(event["cpu"])+1)]}
        ],
        MaxResults=100,
    )
    print("------")
    print(response)
    for instance_ids in response:
        if instance_ids['CurrentGeneration'] == os.environ['bool']:
            instance_id = response['InstanceTypes'][0]['InstanceType']

    return instance_id


def create_launch_template(event):
    # Define parameters
    template_name = event["registry-name"]
    image_id = "ami-0440d3b780d96b29d"
    instance_type = get_instance_id(event)

    # Create Launch Template
    print("creating")
    response = ec2_client.create_launch_template(
        DryRun=False,
        LaunchTemplateName=template_name,
        VersionDescription="Model deploymetn",
        LaunchTemplateData={
            'EbsOptimized': False,
            'IamInstanceProfile': {
                'Arn': 'arn:aws:iam::270932919550:instance-profile/ec2',  # get from params
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
        }
    )
    # Print the response
    print(response['LaunchTemplate']['LaunchTemplateName'])
    return response['LaunchTemplate']['LaunchTemplateName']


def create_asg(event):
    launch_template_name = create_launch_template(event)
    response = client_asg.create_auto_scaling_group(
        AutoScalingGroupName=event["registry-name"],
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


if __name__ == "__main__":
    file_path = "/Users/bhanuteja/ecs-automation/mlops-deployment-ecs/functions/config.json"
    with open(file_path, "r") as file:
        contents = json.loads(file.read())
    lambda_handler(contents, 1)
