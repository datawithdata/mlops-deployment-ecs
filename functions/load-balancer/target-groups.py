import boto3
import json
from decimal import Decimal
import os

client = boto3.client('elbv2')
dynamodb = boto3.resource('dynamodb')


def get_config(event):
    table_name = os.environ['TABLE_NAME']
    table = dynamodb.Table(table_name)
    try:
        # Check if record exists
        response = table.get_item(
            Key={"registry-name": event['registry-name']})
        for version in response['Item']['versions']:
            if version['version'] == Decimal(event['model-version']):
                config = version['config'][0]
        return config
    except Exception as err:
        print(str(err))
    return 1


def create_target_group(event):
    response = client.create_target_group(
        Name=event['registry-name'],
        Protocol='HTTP',
        Port=123,
        VpcId='vpc-0b4da02d066d1e2af',
        HealthCheckProtocol='HTTP',
        HealthCheckPort="5000",
        HealthCheckEnabled=True,
        HealthCheckPath='/health',
        HealthCheckIntervalSeconds=45,
        HealthCheckTimeoutSeconds=10,

        TargetType='instance',
        Tags=[
            {
                'Key': 'string',
                'Value': 'string'
            },
        ],
        IpAddressType='ipv4'
    )
    return response['TargetGroups'][0]['TargetGroupArn']


def create_listner(event, target_group_arn):
    response = client.create_listener(
        LoadBalancerArn=os.environ['LOADBALANCER_ARN'],
        Protocol='HTTP',
        Port=123,
        DefaultActions=[
            {
                'Type': 'forward',
                'TargetGroupArn': target_group_arn,


                'Order': 123,
                'ForwardConfig': {
                    'TargetGroups': [
                        {
                            'TargetGroupArn': target_group_arn,
                            'Weight': 1
                        },
                    ],
                }
            },
        ],
        Tags=[
            {
                'Key': 'string',
                'Value': 'string'
            },
        ],

    )
    return response['Listeners'][0]['ListenerArn']


def lambda_handler(event, context):
    # TODO implement
    # Replace these with your actual values

    config_details = get_config(event)
    print(config_details)
    target_group_arn = create_target_group(event)
    listner_arn = create_listner(event, target_group_arn)

    return {"target_group_arn": target_group_arn, "listner_arn": listner_arn, "config": config_details['config'], "data": event}
