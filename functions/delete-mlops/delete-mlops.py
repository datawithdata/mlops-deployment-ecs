import json
import boto3
import os

client_ec2 = boto3.client('ec2')
client_elb = boto3.client('elbv2')
client_dynamo = boto3.resource('dynamodb')
client_elb = boto3.client('elbv2')
client_asg = boto3.client('autoscaling')
client_ecs = boto3.client('ecs')

def get_details(data):
    table_name = os.environ['TABLE_NAME']
    table = client_dynamo.Table(table_name)
    try:
        # Check if record exists
        response = table.get_item(
            Key={"registry-name": data['registry-name']})
        print(response)
        matching_dicts = list(filter(lambda item: str(item["version"]) == data['version'], response['Item']['versions']))
        matching_dict = list(filter(lambda item: str(item["version"]) == data['ecr-version'], matching_dicts[0]['ECR-info']))
        print(matching_dict)
        del matching_dict[0]['listner_arn']
        del matching_dict[0]['target_group_arn']
        del matching_dict[0]['taskDefinitionArn']
        del matching_dict[0]['predict-url']
        _ = table.update_item(
            Key={"registry-name": data['registry-name']},
            UpdateExpression='SET versions = :versions',
            ExpressionAttributeValues={
                ':versions':  response['Item']['versions']
            }
        )
    except Exception as err:
        print("in error")
        print(str(err))
    
    return matching_dict   

def delete_lb(data):
    print(data)
    try:
        _ = client_elb.delete_listener(ListenerArn=data[0]['listner_arn'])
        _ = client_elb.delete_target_group(TargetGroupArn=data[0]['target_group_arn'])
    except Exception as err:
        print(str(err))
        return "error"
    return "success"

def delete_asg(data): 
    try:
        _ = client_ec2.delete_launch_template(LaunchTemplateName="mlops-"+data['registry-name'])
        _ = client_asg.delete_auto_scaling_group(AutoScalingGroupName="mlops-"+data['registry-name'],ForceDelete=True)
        return 1
    
    except Exception as err:
        print(str(err))
def delete_ecs(data):
    response = client_ecs.delete_service(cluster="mlops-"+data['registry-name'],service=data['registry-name']+"-service",force=True)
    
def lambda_handler(event, context):
    
    # get the LB and target groups
    _ = delete_ecs(event)
    _ = delete_asg(event)
    res=get_details(event)    
    res_lb = delete_lb(res)
    return {
        'statusCode': 200,
        'body': 1
    }