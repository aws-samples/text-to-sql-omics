from aws_cdk import Stack
import aws_cdk as cdk
from constructs import Construct
from aws_cdk import aws_iam as iam
from aws_cdk import aws_ssm as ssm
from Configuration import Configuration
from components.vpc import VpcConstruct
from components.ec2 import EC2Construct
from components.athena import AthenaConstruct
from components.api_gateway import APIGatewayConstruct
from components.lambdas import LambdaConstruct
from cdk_nag import NagSuppressions, NagPackSuppression


class PythonCdkStack(Stack):
    vpc: VpcConstruct
    ec2: EC2Construct
    athena: AthenaConstruct
    apigateway: APIGatewayConstruct
    lambdas: LambdaConstruct

    def __init__(
        self, scope: Construct, construct_id: str, config: Configuration, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.lambdas = LambdaConstruct(scope=self, id="lambdas", config=config)
        self.apigateway = APIGatewayConstruct(
            scope=self, id="apigateway", lambdas=self.lambdas, config=config
        )

        NagSuppressions.add_resource_suppressions(
            self,
            [
                NagPackSuppression(
                    id="CdkNagValidationFailure",
                    reason="Supressing 'parameter referencing an intrinsic function' warning",
                ),
            ],
            apply_to_children=True,
        )
