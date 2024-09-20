from constructs import Construct
from aws_cdk import aws_secretsmanager as secretsmanager
from aws_cdk import aws_logs as logs
from aws_cdk import aws_iam as iam
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_apigateway as apigateway
from lambdas import LambdaConstruct
from cdk_nag import NagSuppressions, NagPackSuppression
from aws_cdk import SecretValue
from aws_cdk import Duration
from aws_cdk import aws_cognito as cognito
import random

import Configuration


class APIGatewayConstruct(Construct):
    api: apigateway.RestApi
    apikey: apigateway.ApiKey
    keysecret: secretsmanager.Secret
    stage: apigateway.Stage

    def __init__(
        self,
        scope: Construct,
        id: str,
        lambdas: LambdaConstruct,
        config: Configuration,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        loggroup = logs.LogGroup(
            self, "APILogs", retention=logs.RetentionDays.ONE_MONTH
        )

        # Import the existing User Pool
        self.existing_user_pool = cognito.UserPool.from_user_pool_id(
            self, "ExistingAmplifyCognitoUserPool",
            user_pool_id=config.cognito_user_pool_id,
        )

        self.cognito_auth = apigateway.CognitoUserPoolsAuthorizer(
            self, "OmicsTextToSqlAuthorizer",
            cognito_user_pools=[self.existing_user_pool]
        )

        self.api = apigateway.RestApi(
            self,
            "omicsTextToSqlAPI",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
                allow_headers=apigateway.Cors.DEFAULT_HEADERS
            ),
            api_key_source_type=apigateway.ApiKeySourceType.HEADER,
            cloud_watch_role=True,
            deploy=True,
            deploy_options=apigateway.StageOptions(
                cache_cluster_enabled=False,
                access_log_destination=apigateway.LogGroupLogDestination(loggroup),
                access_log_format=apigateway.AccessLogFormat.json_with_standard_fields(
                    caller=False,
                    http_method=True,
                    ip=True,
                    protocol=True,
                    request_time=True,
                    resource_path=True,
                    response_length=True,
                    status=True,
                    user=True,
                ),
                stage_name="prod",
                tracing_enabled=True,
                metrics_enabled=True,
            ),
        )

        self.api.root.add_method(
            "ANY",
            apigateway.MockIntegration(
                integration_responses=[
                    apigateway.IntegrationResponse(status_code="200")
                ],
                passthrough_behavior=apigateway.PassthroughBehavior.NEVER,
                request_templates={"application/json": "{ 'statusCode': 200 }"},
            ),
            method_responses=[apigateway.MethodResponse(status_code="200")],
        )

        self.stage = self.api.deployment_stage

        usage_plan = self.api.add_usage_plan(
            "usagePlan", name="omicsTextToSqlAPIUsagePlan"
        )

        usage_plan.add_api_stage(stage=self.stage)

        self.addLambdaToGateway(lambdas.text2sql_lambda, "sqlToTextBase")

        self.suppressNags()

    def addLambdaToGateway(self, lambda_function: lambda_.Function, path: str):
        entity = self.api.root.add_resource(
            path,
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_methods=apigateway.Cors.ALL_METHODS,
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_credentials=True,
                allow_headers=apigateway.Cors.DEFAULT_HEADERS
            ),
        )

        integration = apigateway.LambdaIntegration(
            handler=lambda_function,
            timeout=Duration.seconds(29),
        )

        entity.add_method(
            "POST",
            integration,
            # api_key_required=True,
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorizer=self.cognito_auth,
        )


    def suppressNags(self):
        NagSuppressions.add_resource_suppressions(
            self.api,
            [
                NagPackSuppression(
                    id="AwsSolutions-APIG2",
                    reason="This is a sample code to demonstrate how to deploy a Text-to-SQL workflow, request "
                           "validation must be enabled in API Gateway configuration for production code.",
                ),
                NagPackSuppression(
                    id="AwsSolutions-IAM4",
                    reason="Cloudwatch logs policy is OK here",
                    applies_to=[
                        "Policy::arn:<AWS::Partition>:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs"
                    ],
                ),
                NagPackSuppression(
                    id="AwsSolutions-APIG1", reason="Access logging is enabled"
                ),
                NagPackSuppression(
                    id="AwsSolutions-APIG6", reason="Access logging is enabled"
                ),
                NagPackSuppression(
                    id="AwsSolutions-APIG4", reason="Key authenticication is enabled"
                ),
                NagPackSuppression(
                    id="AwsSolutions-COG4",
                    reason="Cognito user pool not required for mocked methods with no pass through.",
                ),
            ],
            apply_to_children=True,
        )

        NagSuppressions.add_resource_suppressions(
            self.stage,
            [
                NagPackSuppression(
                    id="AwsSolutions-APIG3",
                    reason="WAF not necessaary for private API",
                ),
                NagPackSuppression(
                    id=" AwsSolutions-APIG6",
                    reason="Cloudwatch method implemented for important methods",
                ),
            ],
            apply_to_children=True,
        )
