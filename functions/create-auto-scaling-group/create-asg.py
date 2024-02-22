import json
import boto3 
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
def lambda_handler(event, context):
   
    return {
        'statusCode': 200,
        'body': response
    }
