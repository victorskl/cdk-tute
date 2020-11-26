#!/usr/bin/env python3

from aws_cdk import core

from boiler_app.boiler_app_stack import BoilerAppStack


app = core.App()
BoilerAppStack(app, "boiler-app")

app.synth()
