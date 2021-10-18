import os

from aws_cdk import (
    core,
    aws_ec2 as ec2,
)

# See https://docs.aws.amazon.com/cdk/latest/guide/environments.html
env_profile = core.Environment(
    account=os.environ.get('CDK_DEPLOY_ACCOUNT', os.environ['CDK_DEFAULT_ACCOUNT']),
    region=os.environ.get('CDK_DEPLOY_REGION', os.environ['CDK_DEFAULT_REGION'])
)


class DebugStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, props, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        image = ec2.MachineImage.lookup(
            # name="ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-20211001",
            name="ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*",
            owners=["099720109477"],  # canonical owner id
            filters={
                'architecture': ["x86_64"],
                'virtualization-type': ["hvm"],
            },
        )
        # print(type(image))
        # print(dir(image))
        # print(image)

        image_config: ec2.MachineImageConfig = image.get_image(self)
        print(f"LOOKUP: {image_config.image_id}")
        # print(config.os_type)

        print("-"*64)

        amzn_linux = ec2.MachineImage.latest_amazon_linux(
            cached_in_context=True,
            cpu_type=ec2.AmazonLinuxCpuType.X86_64,
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
        )
        # print(type(amzn_linux))
        # print(dir(amzn_linux))
        # print(amzn_linux)

        amzn_config: ec2.MachineImageConfig = amzn_linux.get_image(self)
        print(f"AMZN_LINUX: {amzn_config.image_id}")


class DebugApp(core.App):
    def __init__(self):
        super().__init__()
        DebugStack(self, "debug-ami-stack", props={}, env=env_profile)


if __name__ == '__main__':
    DebugApp().synth()

# Usage:
#   aws sso login --profile=dev
#   export AWS_PROFILE=dev
#
#   cdk synth --app="python3 ami.py"
#   cdk context -j | jq
#
# (clear context and repeat again)
#   cdk context --clear

# REF:
# https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/README.html#machine-images-amis
# https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/MachineImage.html
# https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/virtualization_types.html
# https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/finding-an-ami.html

# TL;DR is that,
# It might as well be just search through Ec2 Console > Images > AMIs.
# Because, AMI ID better be pinned, rather than dynamically lookup or resolving it through SDK/API call.
# Changes in AMI ID means replacing or recreating the Ec2 instance!
