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


def get_latest_version(response):

    data = response['Item']['versions']
    values = [int(item['version']) for item in data]
    return max(values)+1


def lambda_handler(event, context):
    # TODO implement
    # Replace these with your actual values
    table_name = os.environ['table_name']

    # Get a reference to the table
    table = dynamodb.Table(table_name)
    try:
        # Check if record exists
        response = table.get_item(
            Key={"registry-name": event['registry-name']})
        if 'Item' not in str(response):
            print("Creating new registry")
            event['versions'][0]['version'] = 1
            _ = table.put_item(Item=event)
        else:
            print("update existing registry")
            response['Item']['versions'].append({'version': get_latest_version(
                response), 's3_location': event['versions'][0]['s3_location'], 'Accurecy': event['versions'][0]['Accurecy']})
            response = table.update_item(
                Key={"registry-name": event['registry-name']},
                UpdateExpression='SET versions = :versions',
                ExpressionAttributeValues={
                    ':versions':  response['Item']['versions']
                }
            )
    except Exception as err:
        print(str(err))

    return {
        'statusCode': 200,
        'body': json.dumps('Successfully update')
    }
