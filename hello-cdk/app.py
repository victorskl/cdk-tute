#!/usr/bin/env python3

import aws_cdk as cdk

from hello_cdk.hello_cdk_stack import HelloCdkStack


app = cdk.App()
HelloCdkStack(app, "hello-cdk")

app.synth()
