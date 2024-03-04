
import boto3
ec2_client = boto3.client('ec2')
event = {
    "target_group_arn": "arn:aws:elasticloadbalancing:us-east-1:270932919550:targetgroup/test39/b8910c48a944d050",
    "listner_arn": "arn:aws:elasticloadbalancing:us-east-1:270932919550:listener/app/siri-ml-model/d9923252a8dd2e68/e52ffecc77aaf22b",
    "config": {
        "cpu": "1",
        "version": "3",
        "ram": "2048"
    },
    "data": {
        "registry-name": "test39",
        "model-version": 1,
        "ecr-version": 1,
        "ram": "2048Mi",
        "cpu": "1024m",
        "deployment-type": "deploy"
    }
}

response = ec2_client.describe_instance_types(
    DryRun=False,

    Filters=[
        {"Name": "memory-info.size-in-mib",
         "Values": [event['config']["ram"], str(int(event['config']["ram"])+1)]},
        {"Name": "vcpu-info.default-vcpus",
         "Values": [event['config']["cpu"], str(int(event['config']["cpu"])+1)]}
    ],
    MaxResults=100,
)
print(response)
for instance_ids in response:
    print("In loops")
    print(instance_ids)
    if instance_ids['CurrentGeneration'] == True:
        instance_id = instance_ids['InstanceType']
