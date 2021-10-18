import os

from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_iam as iam,
)

# See https://docs.aws.amazon.com/cdk/latest/guide/environments.html
env_profile = core.Environment(
    account=os.environ.get('CDK_DEPLOY_ACCOUNT', os.environ['CDK_DEFAULT_ACCOUNT']),
    region=os.environ.get('CDK_DEPLOY_REGION', os.environ['CDK_DEFAULT_REGION'])
)

# Console > AMI Search filter
#   owner: 137112412989 (amazon)
#   region: ap-southeast-2
#   virtualization-type: hvm
#   architecture: x86_64
#   root-device-type: ebs
#   creation-date: > September 30, 2021
# Note
#   name: amzn2-ami-hvm-2.0.20211001.1-x86_64-gp2
#    -ebs uses magnetic storage for the root volume
#    -gp2 uses General Purpose (SSD) storage for the root volume
#    root device name is /dev/xvda
ami_id = "ami-05c029a4b57edda9e"

# https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/README.html#machine-images-amis
ami_map = {
    env_profile.region: ami_id,
}

# Block devices:
# https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/README.html#block-devices
# https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/block-device-mapping-concepts.html
# https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/device_naming.html
# https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/nvme-ebs-volumes.html
root_device_name = "/dev/xvda"
data_device_name = "/dev/sdf"


class DebugStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, props, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        my_role = iam.Role(
            self,
            "MyRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"),
            ],
        )

        my_vpc = ec2.Vpc.from_lookup(self, "DefaultVPC", is_default=True)
        my_subnets = ec2.SubnetSelection()  # any subnet that suit

        # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/README.html#user-data
        # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/UserData.html
        my_user_data = ec2.UserData.custom(f"""#!/bin/bash
if [ ! -d "/mnt/data" ]; then
    mkdir -p /mnt/data
    mkfs -t ext4 {data_device_name}
    echo "{data_device_name}       /mnt/data   ext4    rw,user,suid,dev,exec,auto,async 0       2" >> /etc/fstab
    mount -a
fi""")

        # Prepare custom Root volume
        ebs_root_vol = ec2.BlockDeviceVolume.ebs(volume_size=15)  # 15GB
        ebs_root_block_device = ec2.BlockDevice(device_name=root_device_name, volume=ebs_root_vol)

        # Additional volumes
        ebs_data_vol = ec2.BlockDeviceVolume.ebs(volume_size=10)  # 10GB
        ebs_data_block_device = ec2.BlockDevice(device_name=data_device_name, volume=ebs_data_vol)

        my_vm = ec2.Instance(
            self,
            id="MyVM",
            instance_type=ec2.InstanceType("t3.medium"),
            instance_name="my-vm",
            machine_image=ec2.MachineImage.generic_linux(ami_map=ami_map),
            vpc=my_vpc,
            vpc_subnets=my_subnets,
            role=my_role,
            user_data=my_user_data,
            block_devices=[
                ebs_root_block_device,
                ebs_data_block_device,
            ],
        )

        core.CfnOutput(self, "Output", value=my_vm.instance_id)


class DebugApp(core.App):
    def __init__(self):
        super().__init__()
        DebugStack(self, "debug-vm-stack", props={}, env=env_profile)


if __name__ == '__main__':
    DebugApp().synth()

# Usage:
#   aws sso login --profile=dev
#   export AWS_PROFILE=dev
#
#   cdk synth --app="python3 vm.py"
#   cdk context -j | jq
#   cdk diff --app="python3 vm.py"
#   cdk deploy --app="python3 vm.py"
#       aws ssm start-session --target <instance-id>
#         sudo su ec2-user
#
#         df -h
#         Filesystem      Size  Used Avail Use% Mounted on
#         /dev/nvme0n1p1   15G  1.6G   14G  11% /
#         /dev/nvme1n1    9.8G   37M  9.2G   1% /mnt/data
#
#         cat /etc/fstab
#         #
#         UUID=e6c06bf4-70a3-4524-84fa-35484afc0d19     /           xfs    defaults,noatime  1   1
#         /dev/sdf       /mnt/data   ext4    rw,user,suid,dev,exec,auto,async 0       2
#
#         sudo fdisk -l
#
#   cdk destroy --app="python3 vm.py"

# REF:
# https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/README.html

# See also:
# https://github.com/victorskl/terraform-tute/tree/master/aws-ec2
