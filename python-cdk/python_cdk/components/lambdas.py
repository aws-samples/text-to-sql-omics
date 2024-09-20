import os.path as path
from constructs import Construct
from aws_cdk import Duration
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_iam as iam
from aws_cdk import aws_ec2 as ec2
from cdk_nag import NagSuppressions, NagPackSuppression

import Configuration


class LambdaConstruct(Construct):
    lists_role: iam.Role

    text2sql_role: iam.Role
    text2sql_lambda: lambda_.Function

    def __init__(
        self, scope: Construct, id: str, config: Configuration, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        text2sqlEnv = {
            "ATHENA_DB": config.AthenaDatabase,
            "ATHENA_QUERY_RESULTS_BUCKET": config.AthenaResultsBucket,
            "ATHENA_WORKGROUP": config.AthenaWorkgroup,
            "APP_SYNC_URL": config.AppSyncApiUrl,
        }
        (self.text2sql_lambda, self.text2sql_role) = self.buildLambdaDocker(
            "text2sql", "python_cdk/lambda/text2sql", text2sqlEnv, config
        )

    def buildLambdaDocker(
        self, id: str, sourceDir: str, environment: dict, config: Configuration
    ) -> tuple[lambda_.DockerImageFunction, iam.Role]:
        the_role = iam.Role(
            self,
            id + "Role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
        )

        the_lambda = lambda_.DockerImageFunction(
            self,
            id=id,
            code=lambda_.DockerImageCode.from_image_asset(path.join(sourceDir)),
            environment=environment,
            memory_size=512,
            role=the_role,
            timeout=Duration.seconds(600),
        )

        self.lambdaPerms(the_role, config=config)

        return (the_lambda, the_role)

    def lambdaPerms(self, role: iam.Role, config: Configuration):
        role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions= [
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                resources= ["*"]
            ))

        role.add_to_policy(
            iam.PolicyStatement(
                effect= iam.Effect.ALLOW,
                actions= [
                    "xray:PutTraceSegments",
                    "xray:PutTelemetryRecords",
                    "xray:GetSamplingRules",
                    "xray:GetSamplingTargets",
                    "xray:GetSamplingStatisticSummaries"
                ],
                resources= ["*"]
            ))

        role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "bedrock:InvokeModel"
                ],
                resources=[
                    "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-v2",
                    "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"
               ]
            ))

        role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "athena:ListTableMetadata",
                ],
                resources=[
                    "*",
                ]
            ))

        role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "athena:BatchGetQueryExecution",
                    "athena:CancelQueryExecution",
                    "athena:GetCatalogs",
                    "athena:GetExecutionEngine",
                    "athena:GetExecutionEngines",
                    "athena:GetNamespace",
                    "athena:GetNamespaces",
                    "athena:GetQueryExecution",
                    "athena:GetQueryExecutions",
                    "athena:GetQueryResults",
                    "athena:GetQueryResultsStream",
                    "athena:GetTable",
                    "athena:GetTables",
                    "athena:ListQueryExecutions",
                    "athena:RunQuery",
                    "athena:StartQueryExecution",
                    "athena:StopQueryExecution",
                    "athena:ListWorkGroups",
                    "athena:ListEngineVersions",
                    "athena:GetWorkGroup",
                    "athena:GetDataCatalog",
                    "athena:GetDatabase",
                    "athena:GetTableMetadata",
                    "athena:ListDataCatalogs",
                    "athena:ListDatabases",
                    "athena:GetTableMetadata"
                ],
                resources=[
                    f"arn:aws:athena:us-east-1:{config.account}:datacatalog/AwsDataCatalog",
                    f"arn:aws:athena:us-east-1:{config.account}:workgroup/omicsathena"
                ]
            ))
        role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "s3:ListBucket",
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:GetBucketLocation"
                ],
                resources=[
                    f"arn:aws:s3:::{config.AthenaResultsBucket}",
                    f"arn:aws:s3:::{config.AthenaResultsBucket}/*",
                ]
            ))

        role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "glue:GetDatabase",
                    "glue:GetDatabases",
                    "glue:GetTables",
                    "glue:GetTable",
                    "glue:GetPartitions",
                    "athena:ListDataCatalogs",
                    "athena:ListWorkGroups",
                    "athena:GetDatabase",
                    "athena:ListDatabases",
                    "athena:ListTableMetadata",
                    "athena:GetTableMetadata"
                ],
                resources=[
                    "*"
                ]
            ))

        role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "omics:Get*",
                    "omics:List*"
                ],
                resources=[
                    "*"
                ]
            ))

        role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "lakeformation:GetDataAccess"
                ],
                resources=[
                    "*"
                ]
            ))

        NagSuppressions.add_resource_suppressions(
            role,
            [
                NagPackSuppression(
                    id="AwsSolutions-IAM5",
                    reason="Wildcard permissions appropriate here",
                    applies_to=["Resource::*", f"Resource::arn:aws:s3:::{config.AthenaResultsBucket}/*"]
                )
            ],
            apply_to_children=True,
        )

        NagSuppressions.add_resource_suppressions(
            role,
            [
                NagPackSuppression(
                    id="AwsSolutions-IAM5",
                    reason="Wildcard to have read access to omics data.",
                    applies_to=["Action::omics:Get*", "Action::omics:List*"]
                )
            ],
            apply_to_children=True,
        )