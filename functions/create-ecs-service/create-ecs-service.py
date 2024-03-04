import json
import boto3
import os
ecs_client = boto3.client('ecs')
client_asg = boto3.client('autoscaling')


def deploy_service(event):

    desired_count = 2  # Number of tasks to run

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
                'containerPort': 80  # Container port to expose through the load balancer
            }
        ]
    }


try:
    # Create the ECS service
    response = ecs_client.create_service(**service_config)
except Exception as error:
    print(f"Error creating ECS service: {error}")


def lambda_handler(event, context):
    try:
        _ = deploy_service(event)
    except Exception as er:
        print("in error")
        print(str(er))
    return {
        'statusCode': 200,
        'body': 1
    }
