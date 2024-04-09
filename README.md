# AWS ECS auto ML model deployment

Once this repository is deployed within an AWS account, it will automatically provision all necessary components such as Lambdas, Step Functions, API Gateway, DynamoDB, and S3. This setup is designed to streamline and automate the process of deploying Docker images to AWS ECS clusters.

## Table of Contents

- [Installation](#installation)
- [Lambdas](#Lambdas)
- [Python Scripts](#python-scripts)
  - [Script 1](#script-1)
  - [Script 2](#script-2)
- [Contributing](#contributing)
- [License](#license)

## Installation

Ensure that you provide the required values in dev.json, qa.json, and prod.json, such as account IDs, the desired AWS region for automation deployment, VPC configurations, etc.

Once the necessary information is provided, proceed to move your code to the respective branches such as dev, qa, and prod to deploy the ECS automation in each of your environments.

## Lambdas

The majority of our automation is orchestrated through our Lambdas with the assistance of Step Functions. In this section, we'll provide an overview of the high-level functions performed by each Lambda.

  #### <img src="https://github.com/datawithdata/mlops-deployment-ecs/blob/main/logos/lambda.png" width="20" height="20"> **1) load-balancer** 
  
  This function is responsible for creating target groups and listeners within an existing AWS Application Load Balancer. It also dynamically assigns ports for each listener.
  #### <img src="https://github.com/datawithdata/mlops-deployment-ecs/blob/main/logos/lambda.png" width="20" height="20"> **2) create-task-cluster** 
  
  This function is responsible for creating an ECS cluster and registering a task (task definition) that is utilized to deploy a container from Amazon Elastic Container Registry (ECR).
  
  #### <img src="https://github.com/datawithdata/mlops-deployment-ecs/blob/main/logos/lambda.png" width="20" height="20"> **3) create-auto-scaling-group** 
  
  This function handles the creation of two main components:
  
  1) It creates an EC2 Launch Template with configuration details such as instance type and EBS settings.
  2) It sets up EC2 Auto Scaling groups, which are utilized for deploying our ECS containers on EC2 instances, as well as managing scaling operations for increasing and decreasing capacity as needed.
  
  #### <img src="https://github.com/datawithdata/mlops-deployment-ecs/blob/main/logos/lambda.png" width="20" height="20"> **4) create-ecs-service ** 
  
  This function is tasked with deploying a container stored in Amazon Elastic Container Registry (ECR) to an ECS cluster running on EC2 servers, utilizing Auto Scaling Groups previously created by the create-auto-scaling-group function.

  #### <img src="https://github.com/datawithdata/mlops-deployment-ecs/blob/main/logos/lambda.png" width="20" height="20"> **5) dynamo-db-success ** 
  
This function handles the update of DynamoDB with listener ARN, target group ARN, and Load Balancer URL. This update facilitates the retrieval of the Load Balancer URL for predictions and is also employed for deleting the entire ML model deployed, ranging from ECS cluster to listeners and target groups.

  #### <img src="https://github.com/datawithdata/mlops-deployment-ecs/blob/main/logos/lambda.png" width="20" height="20"> **5) send-success-email ** 
  
This function is responsible for sending email notifications upon the successful deployment of a machine learning (ML) model in an ECS cluster.

#### <img src="https://github.com/datawithdata/mlops-deployment-ecs/blob/main/logos/lambda.png" width="20" height="20"> **5) Rollback ** 
  
In the event of any failure during the deployment of the machine learning (ML) model in ECS, this process will initiate a rollback, reverting all steps to their previous states.

#### <img src="https://github.com/datawithdata/mlops-deployment-ecs/blob/main/logos/apigateway.png" width="20" height="20"><img src="https://github.com/datawithdata/mlops-deployment-ecs/blob/main/logos/lambda.png" width="20" height="20"> **5) delete-mlops ** 
  
This function is employed to remove the complete deployment flow, starting from the target group, listeners, auto-scaling group, launch template, and ECS service.
which will be exposed as REST API using API gateway. 

#### <img src="https://github.com/datawithdata/mlops-deployment-ecs/blob/main/logos/apigateway.png" width="20" height="20"><img src="https://github.com/datawithdata/mlops-deployment-ecs/blob/main/logos/lambda.png" width="20" height="20"> **6) model-registry ** 
  
This function is used to register a model in to DynamoDB. 

```bash
{
  "registry-name": "model-registry-name",
  "versions": [
    {
      "s3_location": "Location of the trained ML model in Amazon S3.",
      "Accurecy": { Accuracy information for ML models, with parameters tailored to individual users.
        "auc": 11,
        "Roc": 22
      }
    }
  ]
}

