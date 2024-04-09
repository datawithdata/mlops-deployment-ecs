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

# load-balancer

This function is responsible for creating target groups and listeners within an existing AWS Application Load Balancer. It also dynamically assigns ports for each listener.

```bash
pip install -r requirements.txt
