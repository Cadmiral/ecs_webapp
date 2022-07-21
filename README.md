[![Infrastruture Diagram](https://github.com/Cadmiral/ecs_webapp/blob/main/ecs_fargate.png?raw=true)](https://github.com/Cadmiral/ecs_webapp/blob/main/ecs_fargate.png?raw=true)
# AWS CDK - Web App running on ECS Fargate 

## What is it?

This project deploys a Web App running in AWS ECS Fargate, components are captured in the infrastructure diagram.


## Pre-Reqs:

See instructions on how to  get started with using AWS CDK https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html.

## How it works:

After Pre-reqs instructions:

1. clone the repo 
```bash
    git clone git@github.com:Cadmiral/ecs_webapp.git
```
2. modify config/prod.yaml to match your AWS Account and region
3. bootstrap account
```bash
    cdk bootstrap -c stage="prod"
```
4. deploy the app
```bash
    cdk deploy MyWebApp -c stage="prod"
```

## Configuration:

Configuration files are located in the /config directory.  

prod.yaml - shows an example on how to create additional stages, i.e dev.yaml - you can choose which account to deploy to using the '-c stage="$stage"' flag.

common.yaml - configuration for various parameters that can be easliy extended   