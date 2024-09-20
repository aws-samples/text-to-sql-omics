import boto3
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
import os

REGION = os.environ.get("AWS_REGION")
DATABASE_NAME = os.environ.get("ATHENA_DB")
ATHENA_QUERY_RESULTS_BUCKET = os.environ.get("ATHENA_QUERY_RESULTS_BUCKET")
ATHENA_WORKGROUP = os.environ.get("ATHENA_WORKGROUP")


def get_athena_lc_sqldb_connection(region, athena_db, glue_databucket_name, athena_wkgrp):
    # Integrates with Athena
    athena_url = f"athena.{region}.amazonaws.com"
    athena_port = '443'

    s3stagingathena = f's3://{glue_databucket_name}/athena'
    athena_connection_string = f"awsathena+rest://@{athena_url}:{athena_port}/{athena_db}?s3_staging_dir={s3stagingathena}/&work_group={athena_wkgrp}"
    print("s3stagingathena: ", s3stagingathena)
    print("athena_connection_string: ", athena_connection_string)

    athena_engine = create_engine(athena_connection_string, echo=True)
    # Adds the word 'end' as reserved to use `column_name.end` when generating prompts
    athena_engine.dialect.preparer.reserved_words.add('end')
    athena_db_connection = SQLDatabase(athena_engine)
    # Display a few details about the connected Athena DB like tables and columns
    display_context_details(athena_db_connection, ["clinvar", "genomad", "variants"])

    return athena_db_connection, athena_engine


def display_context_details(athena_db_connection, tables):
    print(athena_db_connection.get_usable_table_names())
    context = athena_db_connection.get_context()
    print(list(context))
    print(context["table_info"])


if __name__ == "__main__":
    region = REGION
    athena_db = DATABASE_NAME
    glue_databucket_name = ATHENA_QUERY_RESULTS_BUCKET
    athena_wkgrp = ATHENA_WORKGROUP
    get_athena_lc_sqldb_connection(region, athena_db, glue_databucket_name, athena_wkgrp)