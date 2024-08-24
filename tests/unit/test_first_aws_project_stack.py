import aws_cdk as core
import aws_cdk.assertions as assertions

from first_aws_project.first_aws_project_stack import FirstAwsProjectStack

# example tests. To run these tests, uncomment this file along with the example
# resource in first_aws_project/first_aws_project_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = FirstAwsProjectStack(app, "first-aws-project")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
