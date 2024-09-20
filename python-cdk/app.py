#!/usr/bin/env python3
import json
import aws_cdk as cdk
from cdk_nag import AwsSolutionsChecks

from python_cdk.python_cdk_stack import PythonCdkStack
from python_cdk.Configuration import Configuration

with open("configuration.json") as f:
    j = json.loads(f.read())

theConfig = Configuration(**j)

app = cdk.App()
stack = PythonCdkStack(
    app,
    theConfig.appname,
    theConfig,
    env=cdk.Environment(account=theConfig.account, region=theConfig.region)
)

cdk.Aspects.of(app).add(AwsSolutionsChecks())

app.synth()

