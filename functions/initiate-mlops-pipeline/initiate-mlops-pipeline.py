#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 11:13:34 2024

@author: bhanuteja
"""

import json
import boto3
import os

client = boto3.client('stepfunctions')

def lambda_handler(event, context):
    # TODO implement
    data=json.loads(event['body'])
    payload=json.dumps(data['config'])
    response = client.start_execution(stateMachineArn=os.environ['STEPFUNCTION_ARN'],input=payload)
    return "Successfully ini"