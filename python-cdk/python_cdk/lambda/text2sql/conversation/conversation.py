import json, boto3, os
from botocore.config import Config

region = os.environ.get("AWS_REGION")

boto_config = Config(
    read_timeout=900,
    connect_timeout=900,
    region_name=region,
    signature_version="v4",
    retries={"max_attempts": 10, "mode": "standard"},
)

bedrock_client = None


def get_bedrock_client():
    global bedrock_client
    if bedrock_client is None:
        bedrock_client = boto3.client(
            service_name="bedrock-runtime", config=boto_config
        )
    return bedrock_client


def invoke_model(prompt):
    modelId = "anthropic.claude-v2"
    accept = "application/json"
    contentType = "application/json"

    body = json.dumps(
        {
            "prompt": prompt,
            "max_tokens_to_sample": 2000,
            "temperature": 0.1,
            "top_p": 0.9,
        }
    )

    response = get_bedrock_client().invoke_model(
        body=body, modelId=modelId, accept=accept, contentType=contentType
    )
    response_body = json.loads(response.get("body").read())

    return response_body


def build_prompt(user_conversation: list[str], extracted_information):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"prompt.txt")) as f:
        prompt_base = f.read()

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"shots.json")) as f:
        shots = json.load(f)

    multishot = ""
    # Add examples to the shots.json file to use the multishot approach
    for shot in shots:
        multishot += "Conversation:\n"
        for line in shot["inputs"]:
            multishot += "\t" + line + "\n"
        multishot += "Question:\n"
        multishot += "<question>" + shot["question"] + "</question>\n"
        multishot += "\n"

    conversation = ""
    for line in user_conversation:
        if line.endswith("\n"):
            conversation += line
        else:
            conversation += line + "\n"

    prompt_base = prompt_base.format(
        XXXX=multishot, AAAA="\n" + extracted_information, BBBB=conversation
    )

    return prompt_base


if __name__ == "__main__":
    conversation = [
        "Please tell me about gene CHKB",
        "What are the common variants?",
        "Are there any common lof variants greater than alternate allele frequency 0.00015?",
    ]

    prompt = build_prompt(conversation)

    response = invoke_model(prompt)

    print(response["completion"])
