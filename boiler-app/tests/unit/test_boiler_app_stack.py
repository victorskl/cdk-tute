import aws_cdk as core
import aws_cdk.assertions as assertions

from boiler_app.boiler_app_stack import BoilerAppStack


# example tests. To run these tests, uncomment this file along with the example
# resource in boiler_app/boiler_app_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = BoilerAppStack(app, "boiler-app")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::SQS::Queue", {
        "VisibilityTimeout": 300
    })
