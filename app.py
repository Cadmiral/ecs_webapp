#!/usr/bin/env python3
import os
import sys
import aws_cdk as cdk

from lib.mywebapp_stack import MyWebApp
from utils import config_util

app = cdk.App()

# Get target stage from cdk context
stage = app.node.try_get_context('stage')
if stage is None or stage == "unknown":
    sys.exit('You need to set the target stage.'
             ' USAGE: cdk <command> -c stage=dev <stack>')

config = config_util.load_config(stage)
env = cdk.Environment(account=config['awsAccount'],
                      region=config["awsRegion"],
                     )

mywebapp_stack = MyWebApp(app, 
                        "MyWebApp", 
                        config=config,
                        env=env)

app.synth()
