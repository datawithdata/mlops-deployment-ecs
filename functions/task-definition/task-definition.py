#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 15:18:24 2024

@author: bhanuteja
"""

import json
import boto3
import os

client = boto3.client('ecs')
dynamodb = boto3.resource('dynamodb')


def get_registry_info(event):
    table_name = "siri-model-registry"
    table = dynamodb.Table(table_name)
    response = table.get_item(
        Key={"registry-name": event['registry-name']})
    version_lst = []
    for versions in response['Item']['versions']:
        if versions['version'] == event['model-version']:
            print(versions)
            version_lst = versions['ECR-info']
            ecr_location = versions['ECR-info'][0]['ecr-name']
    versions = [int(ver_lst['version']) for ver_lst in version_lst]
    versions.sort()
    return [versions, ecr_location]


def register_task(event):
    version = ""
    version_info = get_registry_info(event)
    print("-----")
    print(version_info)
    ecr_location = version_info[1]
    if event['ecr-version'] == "latest":
        version = str(version_info[0][-1])
    else:
        version = event['ecr-version']
    # Define your task definition details
    task_definition = {
        "family": event['registry-name'],
        "cpu": event['cpu'],
        "memory": event['memory'],
        "networkMode": "awsvpc",
        "requiresCompatibilities": ["EC2"],
        "containerDefinitions": [
            {
                # Replace with your container name
                "name": event['registry-name'],
                # Replace with your image URI
                "image": ecr_location+":"+str(version[-1]),
                "portMappings": [
                    {
                        "containerPort": 80,  # Replace with your container port
                        "hostPort": 80  # Replace with your desired host port
                    }
                ]
            }
        ]
    }

    response = client.register_task_definition(**task_definition)
    return response


def create_cluster(event):

    response = client.create_cluster(
        clusterName=event['registry-name'],
        tags=[
            {
                'key': 'string',
                'value': 'string'
            },
        ],
        settings=[
            {
                'name': 'containerInsights',
                'value': 'enabled'
            },
        ],
        configuration={
            'executeCommandConfiguration': {
                'logging': 'OVERRIDE',
                'logConfiguration': {
                    'cloudWatchLogGroupName': event['registry-name']+"-logs",
                    'cloudWatchEncryptionEnabled': False,
                }
            }
        },

    )
    return 1


def lambda_handler(event, context):
    # TODO implement
    # Replace these with your actual values

    _ = register_task(event)
    _ = create_cluster(event)

    return {
        'statusCode': 200,
        'body': json.dumps('Successfully update')
    }


if __name__ == "__main__":
    file_path = "/Users/bhanuteja/ecs-automation/mlops-deployment-ecs/functions/config.json"
    with open(file_path, "r") as file:
        contents = json.loads(file.read())
    lambda_handler(contents, 1)
