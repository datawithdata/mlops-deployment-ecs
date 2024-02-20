#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 15:18:24 2024

@author: bhanuteja
"""

import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import os

dynamodb = boto3.resource('dynamodb')


def update_dynamodb(contents):
    # Get a reference to the table
    table_name = "siri-model-registry"
    table = dynamodb.Table(table_name)
    try:
        # Check if record exists
        response = table.get_item(
            Key={"registry-name": contents['registry-name']})

        print("update existing registry")
        for version in response['Item']['versions']:
            if version['version'] == contents['version']:
                print(version)
                if version.get('ECR-info'):
                    print("update")
                    version['ECR-info'].append(
                        {"version": os.environ['MY_VAR'], "ecr-name": os.environ.get("REPOSITORY_NAME").split("/")[1]})
                else:
                    print("in else")
                    version["ECR-info"] = []
                    version["ECR-info"].append({"version": os.environ['MY_VAR'],
                                               "ecr-name": os.environ.get("REPOSITORY_NAME").split("/")[1]})
        response = table.update_item(
            Key={"registry-name": contents['registry-name']},
            UpdateExpression='SET versions = :versions',
            ExpressionAttributeValues={
                ':versions':  response['Item']['versions']
            }
        )
    except Exception as err:
        print(str(err))


def lambda_handler():
    # TODO implement
    # Replace these with your actual values
    file_path = "config.json"
    with open(file_path, "r") as file:
        contents = json.loads(file.read())
    _ = update_dynamodb(contents)

    return {
        'statusCode': 200,
        'body': json.dumps('Successfully update')
    }


if __name__ == "__main__":
    lambda_handler()
