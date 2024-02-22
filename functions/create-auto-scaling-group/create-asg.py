import json
import boto3 
ec2_client = boto3.client('ec2', region_name='your-region')


def get_instance_id(event):
     # TODO implement
    client = boto3.client('ec2')
    response = client.describe_instance_types(
                DryRun=False,
               
                Filters=[
                    {"Name": "memory-info.size-in-mib", "Values": list(event["ram"])},
                    {"Name": "vcpu-info.default-vcpus", "Values": list(event["cpu"])}
                ],
                MaxResults=100,
            )
    
    return response['body']['InstanceTypes'][0]['InstanceType']

def create_launch_template(event):
    # Define parameters
    template_name = "my-launch-template"
    image_id = "ami-0123456789abcdef"
    instance_type = get_instance_id(event)

    # Create Launch Template
    response = ec2_client.create_launch_template(
        LaunchTemplateName=template_name,
        ImageId=image_id,
        InstanceType=instance_type,
        'BlockDeviceMappings': [
        {
            'DeviceName': '/dev/xvda',
            'Ebs': {
                'VolumeSize': 120
            }
        }
             ]
        )

    # Print the response
    print(f"Launch Template created: {response['LaunchTemplateName']}")


def create_asg():

    return 1

def lambda_handler(event, context):
   
    return {
        'statusCode': 200,
        'body': response
    }
