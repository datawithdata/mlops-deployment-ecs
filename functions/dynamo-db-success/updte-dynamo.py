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
import sys

dynamodb = boto3.resource('dynamodb')


def update_dynamodb(contents):
    # Get a reference to the table
    table_name = os.environ['TABLE_NAME']
    table = dynamodb.Table(table_name)
    try:
        # Check if record exists
        response = table.get_item(
            Key={"registry-name": contents['registry-name']})

        print("update existing registry")
        for version in response['Item']['versions']:
            if version['version'] == contents['model-version']:
                matching_dicts = list(filter(lambda item: item["version"] == contents['ecr-version'], version['ECR-info']))
                print(version)
                if matching_dicts:
                    matching_dict = matching_dicts[0]  # First matching dictionary
                    matching_dict["listner_arn"] = contents['listner_arn']  
                    matching_dict["target_group_arn"] = contents['target_group_arn']  
                    matching_dict['taskDefinitionArn'] = contents['taskDefinitionArn']
                    matching_dict['predict-url'] = contents['loadbalancer_dns']+":"+contents['port']
                else:
                    print("No dictionary with value of 'a' equal to 1 found.")
                
        response = table.update_item(
            Key={"registry-name": contents['registry-name']},
            UpdateExpression='SET versions = :versions',
            ExpressionAttributeValues={
                ':versions':  response['Item']['versions']
            }
        )
    except Exception as err:
        print(str(err))


def lambda_handler(event, context):
    # TODO implement
    # Replace these with your actual values
    _ = update_dynamodb(event)

    return {
        'statusCode': 200,
        'body': json.dumps('Successfully update')
    }


if __name__ == "__main__":
    lambda_handler()
