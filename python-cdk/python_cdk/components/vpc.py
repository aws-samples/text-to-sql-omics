from constructs import Construct
from aws_cdk import aws_ec2 as ec2
from python_cdk.Configuration import Configuration


class VpcConstruct(Construct):
    def __init__(
        self, scope: Construct, id: str, config: Configuration, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        if config.VPCID is None:
            self.buildVPC(id, config)
        else:
            self.vpc = ec2.Vpc.from_lookup("vpc", vpc_id=config.VPCID)
            self.vpcName = self.vpc.vpc_id

        if config.VPCSecurityGroup is None:
            self.securityGroup = ec2.SecurityGroup(
                self,
                "vpcSG",
                vpc=self.vpc,
                description="Security Group for OneMillion VPC",
            )
        else:
            self.securityGroup = ec2.SecurityGroup.from_security_group_id(
                scope=self, id=id, security_group_id=config.VPCSecurityGroup
            )

        self.securityGroupId = self.securityGroup.security_group_id

        self.buildEndpoints(config)

    def buildVPC(self, id: str, config: Configuration):
        self.vpcName = id + "OneMillion"
        self.vpc = ec2.Vpc(
            self,
            self.vpcName,
            ip_addresses=ec2.IpAddresses.cidr(config.VPCCIDR),
            max_azs=config.MAXAZs,
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC, name="Public", cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    name="Private",
                    cidr_mask=24,
                ),
            ],
            flow_logs={
                "logs": {
                    "trafficType": ec2.FlowLogTrafficType.REJECT,
                },
            },
            enable_dns_hostnames=True,
            enable_dns_support=True,
        )

    def buildEndpoints(self, config: Configuration):
        self.vpcEndpointSSM = self.vpc.add_interface_endpoint(
            "ssmendpoint",
            service=ec2.InterfaceVpcEndpointAwsService.SSM,
            subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)
        )

        self.vpcEndpointSecretsManager = self.vpc.add_interface_endpoint(
            "smendpoint",
            service=ec2.InterfaceVpcEndpointAwsService.SECRETS_MANAGER,
            subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)
        )

        self.vpcEndpointAthena = self.vpc.add_interface_endpoint(
            "athenaendpoint",
            service=ec2.InterfaceVpcEndpointAwsService.ATHENA,
            subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)
        )

        self.vpcEndpointGlue = self.vpc.add_interface_endpoint(
            "glueendpoint",
            service=ec2.InterfaceVpcEndpointAwsService.GLUE,
            subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)
        )

        self.vpcEndpointBedrock = self.vpc.add_interface_endpoint(
            "bedrockendpoint",
            service=ec2.InterfaceVpcEndpointAwsService("bedrock"),
            subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)
        )

        self.vpcEndpointBedrock = self.vpc.add_interface_endpoint(
            "bedrockruntimeendpoint",
            service=ec2.InterfaceVpcEndpointAwsService("bedrock-runtime"),
            subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)
        )

        self.vpcEndpointBedrock = self.vpc.add_interface_endpoint(
            "bedrockagentendpoint",
            service=ec2.InterfaceVpcEndpointAwsService("bedrock-agent"),
            subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)
        )

        self.vpcEndpointBedrock = self.vpc.add_interface_endpoint(
            "bedrockagentruntimeendpoint",
            service=ec2.InterfaceVpcEndpointAwsService("bedrock-agent-runtime"),
            subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)
        )

        self.vpcEndpointAPIGateway = self.vpc.add_interface_endpoint(
            "apigatewayendpoint",
            service=ec2.InterfaceVpcEndpointAwsService.APIGATEWAY,
            subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)
        )

        self.vpcEndpointXRay  = self.vpc.add_interface_endpoint(
            "xrayendpoint",
            service=ec2.InterfaceVpcEndpointAwsService.XRAY,
            subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)
        )

        self.vpcEndpointEc2Messages  = self.vpc.add_interface_endpoint(
            "ec2messagesendpoint",
            service=ec2.InterfaceVpcEndpointAwsService.EC2_MESSAGES,
            subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)
        )

        self.vpcEndpointSsmMessages  = self.vpc.add_interface_endpoint(
            "ssmmessagesendpoint",
            service=ec2.InterfaceVpcEndpointAwsService.SSM_MESSAGES,
            subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)
        )

        self.vpcGatewayS3 = self.vpc.add_gateway_endpoint(
            "s3endpoint",
            service=ec2.GatewayVpcEndpointAwsService.S3,
            subnets=[ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)],
        )

        self.vpcGatewayLambda = self.vpc.add_interface_endpoint(
            "lambdaendpoint",
            service=ec2.InterfaceVpcEndpointAwsService.LAMBDA_,
            subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED),
        )

        self.vpcGatewayAppSync = self.vpc.add_interface_endpoint(
            "appsyncendpoint",
            service=ec2.InterfaceVpcEndpointAwsService.APP_SYNC,
            subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED),
        )
