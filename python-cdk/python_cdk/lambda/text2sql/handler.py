import boto3, json, os, time, io, csv, sys
from botocore.config import Config
import logging
from conversation.conversation import build_prompt, invoke_model
from app.main_sql_generator import OmicsSqlGenerator
import timeit
import app.chat_session
from app.logger_util import logger

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
region = os.environ.get("AWS_REGION")

bedrock_client = None
lambda_client = None

boto_config = Config(
    read_timeout=900,
    connect_timeout=900,
    region_name=region,
    signature_version="v4",
    retries={"max_attempts": 10, "mode": "standard"},
)


def get_bedrock_client():
    global bedrock_client
    if bedrock_client is None:
        bedrock_client = boto3.client(
            service_name="bedrock-runtime", config=boto_config
        )
    return bedrock_client


def get_lambda_client():
    global lambda_client
    if lambda_client is None:
        lambda_client = boto3.client(service_name="lambda", config=boto_config)
    return lambda_client


def lambda_handler(event, context):
    logger.info(event)
    if "body" in event.keys():
        if type(event["body"]) is type({}):
            body_data = event["body"]
        else:
            body = event["body"]
            body_data = json.loads(body)
    elif "conversation" in event.keys():
        body_data = event

    start = timeit.default_timer()

    session_id = body_data["session_id"]
    if session_id is None:
        raise Exception("session_id is required")

    wordSalad = []
    if type(body_data["conversation"]) is list:
        for x in body_data["conversation"]:
            wordSalad.extend(x.split(" "))
        wordSalad = list(set(wordSalad))
    else:
        wordSalad = body_data["conversation"]

    translator = str.maketrans("", "", "?")
    wordSalad = [x.translate(translator) for x in wordSalad]

    variants = {}

    # this can be used to provide consolidated gene names or variant names to facilitate for the generation process
    # Needs to be implemented
    # e.g.:
    #     genes = "..."
    #     variants = "..."
    #     additional_data = "the gene name is ... the variant name is ..."
    genes = ""
    variants = ""
    additional_data = ""
    logger.info(f"wordSalad: {wordSalad}")
    logger.info(f"body_data[conversation]: {body_data['conversation']}")
    logger.info(wordSalad)
    if type(body_data["conversation"]) is list:
        prompt_input = build_prompt(body_data["conversation"], additional_data)
    else:
        prompt_input = build_prompt(body_data["conversation"], "")

    single_question = invoke_model(prompt_input)["completion"]
    single_question = single_question.split("<question>")[1].split("</question>")[0]

    logger.info(single_question)

    end = timeit.default_timer()
    processing_time = end - start

    main_response = OmicsSqlGenerator().generate_sql_query(single_question)

    csv_buff = io.StringIO()
    if type(main_response["sql_result_set"]) != str:
        logger.info(main_response["sql_result_set"].shape)
        main_response["sql_result_set"].to_csv(csv_buff, index=False)
    else:
        csv_buff.write(main_response["sql_result_set"])

    response = {
        "question": main_response["question"],
        "csv_data": csv_buff.getvalue(),
        "input_conversation": body_data["conversation"],
        "genesfound": genes,
        "variantsFound": variants,
        "timing": {
            "question_creation": processing_time,
            "sql_generation": main_response["processing_time"],
        },
        "full_answer": main_response["full_answer"],
        "sql": main_response["sql"],
    }

    logger.info(f"Final response to submit to AppSync session: {response}")

    end = timeit.default_timer()
    processing_time = end - start

    logger.info(f"Elapsed time: {processing_time}")
    logger.info(f"Session ID: {session_id}")

    cognito_token = event["headers"]["Authorization"]
    session = app.chat_session.ChatSession(session_id, cognito_token)
    logger.info(f"session: {session}")
    session.add_and_upload_new_message(response)

    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            "Content-Type": "application/json",
        },
        "body": json.dumps({"model_response": response}),
    }


if __name__ == "__main__":
    questions = [
        # "Return all variants that are associated with `Non-small_cell_lung_carcinoma` with `drug_response` clinical significance.",
        "What is the frequency of a variant '1:129401111:T:G'?"
    ]
    response = lambda_handler({
        'headers': {
            'Authorization': 'Bearer <PLACEHOLDER>',
        },
        "conversation": questions,
        "session_id":  "docaq-ugefa-xaval", # DynamoDB existing UI chat session. This is for test purpose only after the application was deplooyed.
    }, None)
    logger.info(json.dumps(response, indent=4))
