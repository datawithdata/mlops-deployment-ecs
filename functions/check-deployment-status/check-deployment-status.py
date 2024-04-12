import json
import boto3
client = boto3.client('ecs')

def lambda_handler(event, context):
    # TODO implement
    response = client.describe_services(cluster="mlops-"+event['data']['registry-name'],services=[event['data']["registry-name"]+"-service"])
    
    if response['services'][0]['desiredCount']==response['services'][0]['runningCount']:
        return_val = "deployed"
    else:
        return_val = "Inprogress"
    
    return return_val
