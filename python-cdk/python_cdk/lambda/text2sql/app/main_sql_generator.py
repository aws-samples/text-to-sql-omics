import csv
import re
import uuid
import os

import boto3
from botocore.config import Config
from langchain.chains import create_sql_query_chain
from langchain.chains.llm import LLMChain
from langchain.globals import set_debug

from langchain_aws.chat_models import ChatBedrock
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)

from athena_connection import (get_athena_lc_sqldb_connection)
from table_prompt import gnomad_prompt, variants_prompt, clinvar_prompt
from question_query_category_examples import examples
from utils import boto_clients
from llm_system_prompt import system_prefix
from logger_util import logger

from sqlalchemy.sql import text
import pandas as pd
import timeit

from langchain.globals import set_debug

set_debug(True)

REGION = os.environ.get("AWS_REGION")
DATABASE_NAME = os.environ.get("ATHENA_DB")
ATHENA_QUERY_RESULTS_BUCKET = os.environ.get("ATHENA_QUERY_RESULTS_BUCKET")
ATHENA_WORKGROUP = os.environ.get("ATHENA_WORKGROUP")

def new_bedrock_runtime():
    retry_config = Config(
        region_name=REGION,
        retries={
            'max_attempts': 10,
            'mode': 'standard'
        }
    )
    return boto3.client('bedrock-runtime', config=retry_config)

def extract_sql(text):
    # Regular expression pattern to find content inside <sql_query> tags
    pattern = r'<SQL_QUERY>\s*(.*?)\s*</SQL_QUERY>'
    # Find all matches in the text
    matches = re.findall(pattern, text, re.DOTALL)
    if not matches:
        return None
    # return the last executed query since that should be the one from the 3rd specialist as specified in the prompt.
    return matches[-1]

def execute_query(athena_engine, in_sql_query):

    if in_sql_query is None:
        return "Unable to generate SQL query this time.", None
    query = in_sql_query.replace("\n", '\n')

    with athena_engine.connect() as athena_connection:
        statement = text(query)
        try:
            df_result = pd.read_sql_query(statement, athena_connection)
        except Exception as e:
            logger.error(f"Failure while executing query: [{query}] with error: `{str(e)}`")
            print(e)
            return f"ERROR executing query", str(e)
        athena_connection.close()
        return df_result, None
class OmicsSqlGenerator:
    def __init__(self):
        self.region = REGION
        self.tables_prompt = gnomad_prompt + variants_prompt + clinvar_prompt
        self.athena_db_connection, self.athena_engine = get_athena_lc_sqldb_connection(
            region=self.region,
            athena_db=DATABASE_NAME,
            glue_databucket_name=ATHENA_QUERY_RESULTS_BUCKET,
            athena_wkgrp=ATHENA_WORKGROUP
        )
        self.bedrock_runtime = new_bedrock_runtime()
        model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
        self.llm = ChatBedrock(
            model_id=model_id,
            client=self.bedrock_runtime,
            model_kwargs={
                "temperature": 0,
                "max_tokens": 4096,
                # "top_p": 0.9,
                # "top_k": 250,
                "stop_sequences": ["\n\nHuman:"],
            },
        )

        # self.few_shot_prompt_from_dynamic_few_shot()
        self.few_shot_prompt_from_few_shot()

        self.full_prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate(prompt=self.few_shot_prompt),
                ("human", "<user_input>{input}</user_input>"),
            ]
        )

        # The following snippet can be used in place of the LLMChain to use LangChain SQL chains.
        # That fetches all the tables and column names in the schema and inform the LLM.
        # However, this approach didn't generate the best results and a precise definition of the tables to be used
        # is a better approach.
        # self.chain = create_sql_query_chain(self.llm,
        #                                db=self.athena_db_connection,
        #                                prompt=self.full_prompt)

        logger.info(self.full_prompt)
        self.chain = LLMChain(llm=self.llm, prompt=self.full_prompt)

    def generate_sql_query(self, question):

        start = timeit.default_timer()
        result = self.chain.invoke({
            "input": question,   # this is for when not using langchain sql agents
            # "question": question,
            "top_k": 100,
            "dialect": "awsathena",
            "table_info": self.tables_prompt,
            "verbose": True,
        })["text"] #this is for when not using non langchain sql agents

        logger.info(result)
        sql = extract_sql(result)
        sql_result_set, error_message = execute_query(self.athena_engine, sql)
        if error_message:
            sql, sql_result_set = self.attempt_to_correct_sql_with_error(question, sql, error_message)
        end = timeit.default_timer()
        final_answer = {
            "question": question,
            "full_answer": result,
            "sql": sql,
            "sql_result_set": sql_result_set,
            "processing_time": end - start,
        }

        return final_answer

    def attempt_to_correct_sql_with_error(self, question, sql, error_message):
        new_question = (f"{question} The previously generated query threw the following error message `{error_message}. "
                        f"Generate a new SQL that fix that error. The previous SQL was <SQL_QUERY>{sql}</SQL_QUERY>`.")
        result = self.chain.invoke({
            "input": new_question,
            "top_k": 100,
            "dialect": "awsathena",
            "table_info": self.tables_prompt,
            "verbose": True,
        })["text"]
        sql = extract_sql(result)
        sql_result_set, error_message = execute_query(self.athena_engine, sql)
        return sql, sql_result_set

    def few_shot_prompt_from_dynamic_few_shot(self):
        self.embedding = BedrockEmbeddings(
            model_id="amazon.titan-embed-text-v1",
            region_name=self.region,
            client=boto_clients.get_bedrock_client(),
        )
        self.system_prefix = system_prefix
        self.example_selector = SemanticSimilarityExampleSelector.from_examples(
            examples,
            self.embedding,
            FAISS,
            k=5,
            input_keys=["input"],
        )
        self.few_shot_prompt = FewShotPromptTemplate(
            example_selector=self.example_selector,
            # examples=examples,
            example_prompt=PromptTemplate.from_template(
                "<user_input>{input}</user_input>\n<SQL_QUERY>{query}</SQL_QUERY>"
            ),
            input_variables=[
                "input",
                "dialect",
                "top_k",
                "table_info"
            ],
            prefix=system_prefix,
            suffix="<user_input>{input}</user_input>\n<SQL_QUERY>",
        )

    def few_shot_prompt_from_few_shot(self):
        self.system_prefix = system_prefix
        self.few_shot_prompt = FewShotPromptTemplate(
            # example_selector=self.example_selector,
            examples=examples,
            example_prompt=PromptTemplate.from_template(
                "<user_input>{input}</user_input>\n<SQL_QUERY>{query}</SQL_QUERY>"
            ),
            input_variables=[
                "input",
                "dialect",
                "top_k",
                "table_info"
            ],
            prefix=system_prefix,
            suffix="<user_input>{input}</user_input>\n<SQL_QUERY>",
        )


# Main call to instantiate class and execute generate_sql_query
if __name__ == "__main__":
    sql_generator = OmicsSqlGenerator()

    test_questions = [
        "What is the frequency of a variant '1:129401219:C:G'?",
        "Return all variants that are associated with `Non-small_cell_lung_carcinoma` with `drug_response` clinical significance.",
        "List all variants that are in chromossome 12, in position between 129401219 and 129401329, where the allele frequency is higher than 0.1. Make sure to return the filters.",
    ]

    llm_answers = []

    for question in test_questions:
        start = timeit.default_timer()
        answer = sql_generator.generate_sql_query(question)
        llm_answers.append(answer)

    # write out to CSV file
    out_file_name = 'claude-results-dynamic-few-shot' + str(start) + '.csv'
    with open(out_file_name, 'w') as f:
        w = csv.DictWriter(f, llm_answers[0].keys())
        w.writeheader()
        w.writerows(llm_answers)
