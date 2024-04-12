import json
import boto3
import os
ecs_client = boto3.client('ecs')
client_asg = boto3.client('autoscaling')

print(os.environ['SUBNETS'].split(','))
def deploy_service(event):

    desired_count = 1  # Number of tasks to run

    # Define service configuration
    print("mlops-"+event['data']["registry-name"])
    service_config = {
        'cluster': "mlops-"+event['data']["registry-name"],
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
                'securityGroups': [os.environ['SG']],
                'subnets': os.environ['SUBNETS'].split(',')
            }
        },
    }

    try:
        # Create the ECS service
        response = ecs_client.create_service(**service_config)
    except Exception as err:
        print(str(err))
        vals = {"loc":["target_group","listner","task","ECS","launch_tmplate","service"],"registry":event['data']["registry-name"]}
        raise ValueError(json.dumps(vals))

def lambda_handler(event, context):
    try:
        _ = deploy_service(event)
    except Exception as er:
        print("in error")
        print(str(er))
    
    return event