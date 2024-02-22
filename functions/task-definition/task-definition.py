#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 15:18:24 2024

@author: bhanuteja
"""

import json
import boto3
import os

client = boto3.resource('ecs')
dynamodb = boto3.resource('dynamodb')


def get_registry_info(event):
    table_name = "siri-model-registry"
    table = dynamodb.Table(table_name)
    response = table.get_item(
        Key={"registry-name": event['registry-name']})
    version_lst = []
    for versions in response['Item']['versions']:
        if versions['version'] == event['version']:
            version_lst = versions['ECR-info']
            ecr_location = versions['ecr-name']
    versions = [ver_lst['version'] for ver_lst in version_lst]
    return for [versions.sort(),ecr_location]


def register_task(event):
    version = ""
    version_info = get_registry_info(event)
    ecr_location = version_info[1]
    if event['ecr-version'] == "latest":
        version=version_info[0][-1]
    else:
        version = event['ecr-version']
    # Define your task definition details
    task_definition = {
        "family": event['registry-name'],  # Replace with your desired name
        "cpu": event['cpu'],
        "memory": event['memory'],
        "networkMode": "awsvpc",
        "requiresCompatibilities": ["FARGATE", "EC2"],
        "containerDefinitions": [
            {
                # Replace with your container name
                "name": event['registry-name'],
                # Replace with your image URI
                "image": ecr_location+":"+version[-1],
                "portMappings": [
                    {
                        "containerPort": 80,  # Replace with your container port
                        "hostPort": 8080  # Replace with your desired host port
                    }
                ]
            }
        ]
    }

    response = client.register_task_definition(**task_definition)


def lambda_handler(event, context):
    # TODO implement
    # Replace these with your actual values

    _ = register_task(event)

    return {
        'statusCode': 200,
        'body': json.dumps('Successfully update')
    }
