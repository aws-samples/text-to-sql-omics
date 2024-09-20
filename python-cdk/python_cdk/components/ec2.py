from constructs import Construct
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_iam as iam
from python_cdk.Configuration import Configuration
from cdk_nag import NagSuppressions, NagPackSuppression


class EC2Construct(Construct):
    dataAccess: iam.Role
    ec2Instance: ec2.Instance
    ec2KeyPair: ec2.KeyPair

    def __init__(
        self, scope: Construct, id: str, config: Configuration, vpc: ec2.Vpc, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.dataAccess = iam.Role(
            self,
            "dataAccess",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonSSMManagedInstanceCore"
                )
            ],
        )

        self.dataAccess.add_to_policy(
            iam.PolicyStatement.from_json(
                {
                    "Effect": iam.Effect.ALLOW,
                    "Action": ["iam:GetRole", "iam:PassRole"],
                    "Resource": ["arn:aws:iam::" + config.account + ":role/*"],
                }
            )
        )

        self.ec2KeyPair = ec2.KeyPair(self, "DevKeyPair")

        self.ec2Instance = ec2.Instance(
            self,
            id + "Instance",
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.M5, ec2.InstanceSize.LARGE
            ),
            machine_image=ec2.AmazonLinuxImage(
                generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2023
            ),
            vpc=vpc,
            role=self.dataAccess,
            key_pair=self.ec2KeyPair,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/xvda",
                    volume=ec2.BlockDeviceVolume.ebs(
                        50, encrypted=True, delete_on_termination=True
                    ),
                )
            ],
            detailed_monitoring=True,
        )

        NagSuppressions.add_resource_suppressions(
            self.dataAccess,
            [
                NagPackSuppression(
                    id="AwsSolutions-IAM4",
                    reason="SSM Access AWS policy used",
                    applies_to=[
                        "Policy::arn:<AWS::Partition>:iam::aws:policy/AmazonSSMManagedInstanceCore"
                    ],
                ),
                NagPackSuppression(
                    id="AwsSolutions-IAM5",
                    reason="wildcard permission are appropriate for Cloudwatch logging",
                    applies_to=["Resource::arn:aws:iam::" + config.account + ":role/*"],
                ),
            ],
            apply_to_children=True,
        )

        NagSuppressions.add_resource_suppressions(
            self.ec2Instance,
            [
                NagPackSuppression(
                    id="AwsSolutions-EC29",
                    reason="Deletion protection unneeded",
                ),
            ],
            apply_to_children=True,
        )
