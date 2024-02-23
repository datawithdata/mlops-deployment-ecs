import boto3
import json
client = boto3.client('elbv2')


def create_target_group(event):
    response = client.create_target_group(
        Name=event['registry-name'],
        Protocol='HTTP',
        Port=123,
        VpcId='string',
        HealthCheckProtocol='HTTP',
        HealthCheckPort=5000,
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
        LoadBalancerArn='string',
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

    target_group_arn = create_target_group(event)
    listner_arn = create_listner(event, target_group_arn)

    return {"target_group_arn": target_group_arn, "listner_arn": listner_arn}


if __name__ == "__main__":
    file_path = "/Users/bhanuteja/ecs-automation/mlops-deployment-ecs/functions/config.json"
    with open(file_path, "r") as file:
        contents = json.loads(file.read())
    lambda_handler(contents, 1)
