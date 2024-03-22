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
            Key={"registry-name": contents['data']['registry-name']})

        print("update existing registry")
        for version in response['Item']['versions']:
            print(version['version'])
            print(str(contents['data']['model-version']))
            print("---------")
            if str(version['version']) == str(contents['data']['model-version']):
                matching_dicts = list(filter(lambda item: str(item["version"]) == str(contents['data']['ecr-version']), version['ECR-info']))
                print(version)
                print(version['ECR-info'])
                if matching_dicts:
                    matching_dict = matching_dicts[0]  # First matching dictionary
                    matching_dict["listner_arn"] = contents['listner_arn']  
                    matching_dict["target_group_arn"] = contents['target_group_arn']  
                    matching_dict['taskDefinitionArn'] = contents['taskDefinitionArn']
                    matching_dict['predict-url'] = os.environ['LOADBALANCER_NAME']+":"+str(contents['port'])
                else:
                    print("No dictionary match")
                    return "no data"
                
        response = table.update_item(
            Key={"registry-name": contents['data']['registry-name']},
            UpdateExpression='SET versions = :versions',
            ExpressionAttributeValues={
                ':versions':  response['Item']['versions']
            }
        )
        
        return "success"
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


