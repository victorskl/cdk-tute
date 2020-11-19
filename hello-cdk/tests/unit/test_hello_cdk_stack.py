import json
import pytest

from aws_cdk import core
from hello_cdk.hello_cdk_stack import HelloCdkStack


def get_template():
    app = core.App()
    HelloCdkStack(app, "hello-cdk")
    return json.dumps(app.synth().get_stack("hello-cdk").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
