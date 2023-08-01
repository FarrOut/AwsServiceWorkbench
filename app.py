#!/usr/bin/env python3
import os

import aws_cdk as cdk

from aws_service_workbench.aws_service_workbench_stack import AwsServiceWorkbenchStack

app = cdk.App()
AwsServiceWorkbenchStack(app, "AwsServiceWorkbenchStack",
                         env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                                             region=os.getenv('CDK_DEFAULT_REGION')),
                         )

app.synth()
