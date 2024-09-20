from botocore.config import Config
import boto3
import os

region = os.environ.get("AWS_REGION")
print(f"Boto Region: {region}")

bedrock_region = region
dynamo_region = region
kendra_region = region
opensearch_region = region
athena_region = region
secrets_region = region

dynamo_config = Config(
    read_timeout=900,
    connect_timeout=900,
    region_name=region,
    signature_version="v4",
    retries={"max_attempts": 10, "mode": "standard"},
)

secrets_config = Config(
    read_timeout=900,
    connect_timeout=900,
    region_name=region,
    signature_version="v4",
    retries={"max_attempts": 10, "mode": "standard"},
)

bedrock_config = Config(
    read_timeout=900,
    connect_timeout=900,
    region_name=bedrock_region,
    signature_version="v4",
    retries={"max_attempts": 10, "mode": "standard"},
)

kendra_config = Config(
    read_timeout=900,
    connect_timeout=900,
    region_name=kendra_region,
    signature_version="v4",
    retries={"max_attempts": 10, "mode": "standard"},
)

opensearch_config = Config(
    read_timeout=900,
    connect_timeout=900,
    region_name=opensearch_region,
    signature_version="v4",
    retries={"max_attempts": 10, "mode": "standard"},
)

athena_config = Config(
    read_timeout=900,
    connect_timeout=900,
    region_name=athena_region,
    signature_version="v4",
    retries={"max_attempts": 10, "mode": "standard"},
)

dynamodb_client = None
secrets_client = None
bedrock_client = None
kendra_client = None
oss_client = None
athena_client = None


def get_dynamodb_client():
    global dynamodb_client
    if dynamodb_client is None:
        dynamodb_client = boto3.client("dynamodb", config=dynamo_config)

    return dynamodb_client


def get_secrets_client():
    global secrets_client
    if secrets_client is None:
        secrets_client = boto3.client("secretsmanager", config=dynamo_config)

    return secrets_client


def get_dynamo_table(table_name):
    boto3.setup_default_session(region_name=dynamo_region)
    return boto3.resource("dynamodb").Table(table_name)


def get_bedrock_client():
    global bedrock_client
    if bedrock_client is None:
        bedrock_client = boto3.client(
            service_name="bedrock-runtime", config=bedrock_config
        )
    return bedrock_client


def get_kendra_client():
    global kendra_client
    if kendra_client is None:
        kendra_client = boto3.client("kendra", config=kendra_config)

    return kendra_client


def get_oss_client():
    global oss_client
    if oss_client is None:
        oss_client = boto3.client("opensearchserverless", config=opensearch_config)

    return oss_client


def get_athena_client():
    global athena_client
    if athena_client is None:
        athena_client = boto3.client("athena", config=athena_config)

    return athena_client
