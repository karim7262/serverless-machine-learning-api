#!/usr/bin/env python3

from aws_cdk import core

from serverless_machine_learning_api.stacks.back_end.vpc_stack import VpcStack
from serverless_machine_learning_api.stacks.back_end.efs_stack import EfsStack
from serverless_machine_learning_api.stacks.back_end.serverless_machine_learning_api_stack import ServerlessMachineLearningApiStack
from pytorch_loader.custom_resources.stacks.pytorch_on_ec2_stack import PytorchOnEc2Stack

app = core.App()

# VPC Stack for hosting Secure API & Other resources
vpc_stack = VpcStack(
    app,
    "vpc-stack",
    description="Miztiik Automation: VPC to host resources for generating load on API"
)

# Create EFS
efs_stack = EfsStack(
    app,
    "efs-stack",
    vpc=vpc_stack.vpc,
    description="Miztiik Automation: Deploy AWS Elastic File System Stack"
)

# Lambda with EFS for Video Processing
serverless_machine_learning_api = ServerlessMachineLearningApiStack(
    app,
    "serverless-machine-learning-api",
    vpc=vpc_stack.vpc,
    lambda_efs_sg=efs_stack.lambda_efs_sg,
    efs_sg=efs_stack.efs_sg,
    efs_share=efs_stack.efs_share,
    efs_ap=efs_stack.efs_ap,
    efs_ap_ml=efs_stack.efs_ap_ml,
    stack_log_level="INFO",
    back_end_api_name="well-architected-api",
    description="Miztiik Automation: Serverless machine learning API using PyTorch running in AWS Lambda"
)


# Deploy Pytorch on EC2 & EFS(If necessary)
pytorch_on_ec2 = PytorchOnEc2Stack(
    app,
    "pytorch-on-ec2",
    vpc=vpc_stack.vpc,
    ec2_instance_type="m5.large",
    deploy_to_efs=False,
    efs_ap_ml=efs_stack.efs_ap_ml,
    efs_sg=efs_stack.efs_sg,
    stack_log_level="INFO",
    description="Deploy EC2 To Install PyTorch in EFS"
)

# Stack Level Tagging
core.Tag.add(app, key="Owner",
             value=app.node.try_get_context("owner"))
core.Tag.add(app, key="OwnerProfile",
             value=app.node.try_get_context("github_profile"))
core.Tag.add(app, key="Project",
             value=app.node.try_get_context("service_name"))
core.Tag.add(app, key="GithubRepo",
             value=app.node.try_get_context("github_repo_url"))
core.Tag.add(app, key="Udemy",
             value=app.node.try_get_context("udemy_profile"))
core.Tag.add(app, key="SkillShare",
             value=app.node.try_get_context("skill_profile"))
core.Tag.add(app, key="AboutMe",
             value=app.node.try_get_context("about_me"))
core.Tag.add(app, key="BuyMeCoffee",
             value=app.node.try_get_context("ko_fi"))

app.synth()
