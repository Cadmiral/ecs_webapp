import aws_cdk as core
import aws_cdk.assertions as assertions

from cloud303.cloud303_stack import Cloud303Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in cloud303/cloud303_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Cloud303Stack(app, "cloud303")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
