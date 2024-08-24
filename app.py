#!/usr/bin/env python3
import os

import aws_cdk as cdk

from first_aws_project.first_aws_project_stack import FirstAwsProjectStack


app = cdk.App()
FirstAwsProjectStack(app, "FirstAwsProjectStack",
    env=cdk.Environment(account='314146310697', region='us-east-1'),
    )

app.synth()
