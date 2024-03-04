import json
import boto3

client_lb = boto3.client("elbv2")


def create_target_group(event):
    response = client_lb.create_target_group(
        Name=event["service_name"],
        Protocol="HTTP",
        ProtocolVersion="HTTP1",
        Port=80,
        VpcId="vpc-0b4da02d066d1e2af",
        HealthCheckProtocol="HTTP",
        HealthCheckPort="5000",
        HealthCheckEnabled=True,
        HealthCheckPath="/health",
        HealthCheckIntervalSeconds=30,
        HealthCheckTimeoutSeconds=25,
        TargetType="ip",
        IpAddressType="ipv4",
    )

    return response["TargetGroups"][0]["TargetGroupArn"]


def create_listner(TargetGroupArn):
    response = client_lb.create_listener(
        LoadBalancerArn="arn:aws:elasticloadbalancing:us-east-1:270932919550:loadbalancer/app/ecs-deploy/dfae2b28512e1f27",
        Protocol="HTTP",
        Port=5000,
        DefaultActions=[
            {
                "Type": "forward",
                "TargetGroupArn": TargetGroupArn,
                "Order": 1,
                "ForwardConfig": {
                    "TargetGroups": [
                        {"TargetGroupArn": TargetGroupArn, "Weight": 1},
                    ],
                },
            },
        ],
    )


def lambda_handler(event, context):
    res = create_target_group(event)
    _ = create_listner(res)
    # TODO implement
    return {"statusCode": 200, "body": json.dumps("Hello from Lambda!")}
