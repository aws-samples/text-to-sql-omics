from constructs import Construct
from aws_cdk import aws_secretsmanager as secretsmanager
from aws_cdk import aws_s3 as s3
from python_cdk.Configuration import Configuration
from aws_cdk import SecretValue
from cdk_nag import NagSuppressions, NagPackSuppression


class AthenaConstruct(Construct):
    athenaSecret: secretsmanager.Secret
    dataBucket: s3.IBucket
    queryBucket: s3.IBucket

    athena_wkgrp: str
    athena_db: str
    athena_region: str
    athena_port = 443

    def __init__(
        self, scope: Construct, id: str, config: Configuration, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.athena_region = config.AthenaRegion
        self.athena_wkgrp = config.AthenaWorkgroup
        self.athena_db = config.AthenaDatabase

        s3stagingathena = "s3://" + config.AthenaResultsBucket + "/athena-results/"

        self.dataBucket = s3.Bucket.from_bucket_name(
            self, "dataBucket", config.AthenaSourceBucket
        )
        self.queryBucket = s3.Bucket.from_bucket_name(
            self, "queryBucket", config.AthenaResultsBucket
        )

        self.athenaSecret = secretsmanager.Secret(
            self,
            "oneMillionPythonAthenaSecret",
            secret_object_value={
                "region": SecretValue(self.athena_region),
                "athena_port": SecretValue(self.athena_port),
                "athena_db": SecretValue(self.athena_db),
                "s3stagingathena": SecretValue(s3stagingathena),
                "athena_wkgrp": SecretValue(self.athena_wkgrp),
            },
        )
