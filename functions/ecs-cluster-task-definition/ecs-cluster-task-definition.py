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
        Key={"registry-name": event['data']['registry-name']})
    version_lst = []
    for versions in response['Item']['versions']:
        if versions['version'] == event['data']['model-version']:
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
    if event['data']['ecr-version'] == "latest":
        version = str(version_info[0][-1])
    else:
        version = event['data']['ecr-version']
    # Define your task definition details
    task_definition = {
        "family": event['data']['registry-name'],
        "cpu": str(int(event['data']['cpu'])*1024),
        "memory": event['data']['ram'],
        "networkMode": "awsvpc",
        "requiresCompatibilities": ["EC2"],
        "containerDefinitions": [
            {
                # Replace with your container name
                "name": event['data']['registry-name'],
                # Replace with your image URI
                "image": ecr_location+":"+str(version),
                "portMappings": [
                    {
                        "containerPort": 80,  # Replace with your container port
                        "hostPort": 80  # Replace with your desired host port
                    }
                ],
                "cpu": int(event['data']['cpu'])*1024,
                "memory": int(event['data']['ram'])
            }
        ]
    }

    response = client.register_task_definition(**task_definition)
    return response


def create_cluster(event):

    response = client.create_cluster(
        clusterName=event['data']['registry-name'],
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
                    'cloudWatchLogGroupName': event['data']['registry-name']+"-logs",
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

    return event
