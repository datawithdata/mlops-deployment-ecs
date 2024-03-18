import json
import boto3

load_balancer = boto3.client('elbv2')
ecs = boto3.client('ecs')
ec2_client = boto3.client('ec2')
client_asg = boto3.client('autoscaling')


def target_listner(event):
    try:
        res_listner = load_balancer.delete_listener(
            ListenerArn=event['listner_arn'])
        print(res_listner)
        res_target = load_balancer.delete_target_group(
            TargetGroupArn=event['target_group_arn'])
        print(res_target)
    except Exception as err:
        print("In target listner")
        print(err)


def asg(event):
    response = client_asg.delete_auto_scaling_group(
        AutoScalingGroupName=event['registry-name'], ForceDelete=True)
    return 1


def delete_service(event):
    response = ec2_client.delete_service(
        cluster=event['registry-name'], service=event['registry-name'], force=True)
    return 1


def lambda_handler(event, context):
    # TODO implement
    print(event)
    vals = json.loads(event['Cause'])
    print(vals['errorMessage'])

    if len(vals['errorMessage']['loc']) == 1:
        return "success"

    elif len(vals['errorMessage']['loc']) == 2:
        _ = target_listner(event)

    elif len(vals['errorMessage']['loc']) == 4 or len(vals['errorMessage']['loc']) == 5:
        _ = asg(event)
    
    elif len(vals['errorMessage']['loc']) == 6:
        _ = delete_service(event)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
