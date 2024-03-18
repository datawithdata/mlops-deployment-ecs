import json
import boto3
import os
ecs_client = boto3.client('ecs')
client_asg = boto3.client('autoscaling')


def deploy_service(event):

    desired_count = 1  # Number of tasks to run

    # Define service configuration
    service_config = {
        'cluster': event['data']["registry-name"],
        'serviceName': event['data']["registry-name"]+"-service",
        'taskDefinition': event['taskDefinitionArn'],
        'desiredCount': desired_count,
        'launchType': 'EC2',  # Can be 'FARGATE' for serverless tasks
        'loadBalancers': [  # Optional: Configure load balancers for the service
            {
                'targetGroupArn': event['target_group_arn'],
                'containerName': event['data']["registry-name"],
                'containerPort': 5000 # Container port to expose through the load balancer
            }
        ],
        'networkConfiguration': {
            'awsvpcConfiguration': {
                'securityGroups': ['sg-0aeecd47559449290'],
                'subnets': ['subnet-046ece9627560a66a','subnet-030e86ba4defd393f','subnet-0b163826522f34c48']
            }
        },
    }

    try:
        # Create the ECS service
        response = ecs_client.create_service(**service_config)
    except Exception as err:
        vals = {"loc":["target_group","listner","task","ECS","launch_tmplate","service"],"registry":event['data']["registry-name"]}
        raise ValueError(json.dumps(vals))

def lambda_handler(event, context):
    try:
        _ = deploy_service(event)
    except Exception as er:
        print("in error")
        print(str(er))
        raise 
   
    return {
        'statusCode': 200,
        'body': 1
    }
