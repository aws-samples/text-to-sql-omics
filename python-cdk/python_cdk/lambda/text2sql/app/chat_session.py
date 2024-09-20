# Class that update an object to AWS AppSync.
# This class will have methods to fetch a Session object and a method to update the Session object.
import os
from datetime import datetime

import requests
import json
from logger_util import logger

# Default AppSync URL
APPSYNC_URL = os.getenv('APP_SYNC_URL')


class ChatSession:
    """
    Class that update an object to AWS AppSync.
    This class will have methods to fetch a Session object and a method to update the Session object.
    """
    def __init__(self, session_id, cognito_token):
        self.id = session_id
        self.cognito_token = cognito_token
        self.messages = []
        query, variables = self.session_query(session_id)
        print(query, variables)
        self.session_data = self.execute_app_sync_call(query, variables)
        if (self.session_data and "data" in self.session_data
                and "getSession" in self.session_data["data"]
                and "messages" in self.session_data["data"]["getSession"]):
            self.messages = self.session_data["data"]["getSession"]["messages"]
        else:
            raise Exception(f"Session data not valid or missing keys")

    def session_query(self, session_id):
        query = """
            query GetSession($id: ID!) {
              getSession(id: $id) {
                id
                messages
              }
            }
            """
        variables = {
            "id": session_id,
        }
        return query, variables

    def execute_app_sync_call(self, statement, variables):
        """
        Execute the GraphQL statement and returns the JSON response as a dict.

        :param statement: The statement to be executed against the GraphQL API
        :param variables: The variables to be passed to the statement
        :return: Return a dict representing the JSON object
        """
        # Set up the request headers
        headers = {
            "Content-Type": "application/graphql",
            "Authorization": self.cognito_token
        }
        response = requests.post(
            APPSYNC_URL,
            headers=headers,
            json={"query": statement, "variables": variables},
            timeout=60
        )
        # Print the response
        print(json.dumps(response.json(), indent=4))
        return json.loads(json.dumps(response.json()))

    def add_and_upload_new_message(self, new_message):
        self.format_and_add_message(new_message)
        mutation, variables = self.upload_messages_mutation()
        try:
            self.session_data = self.execute_app_sync_call(mutation, variables)
            logger.info(f"Message uploaded to AppSync successfully. Message: {self.session_data}")
        except Exception as e:
            logger.error("Error uploading to AppSync:", e)

    def format_and_add_message(self, new_message):
        formatted_new_message = self.format_message(new_message)
        self.messages.append(formatted_new_message)

    def format_message(self, new_message):
        csv_data = new_message["csv_data"]

        formatted_new_message = {
            "value": csv_data,
            "type": "Bot",
            "date": datetime.now().isoformat(),
            "question": new_message["question"],
            "input_conversation": new_message["input_conversation"],
            "genesfound": new_message["genesfound"],
            "variantsFound": new_message["variantsFound"],
            "timing": new_message["timing"],
            "full_answer": new_message["full_answer"],
            "sql": new_message["sql"],
        }
        return json.dumps(formatted_new_message)

    def upload_messages_mutation(self):
        mutation = """
            mutation UpdateSession(
              $input: UpdateSessionInput!
              $condition: ModelSessionConditionInput
            ) {
              updateSession(input: $input, condition: $condition) {
                id
                messages
              }
            }
        """
        variables = {
            "input": {
                "id": self.id,
                "messages": self.messages
            }
        }
        return mutation, variables


if __name__ == "__main__":
    # Create a new ChatSession object
    session = ChatSession(
        "zaduh-ujehe-sosak",
        "Bearer <PLACEHOLDER>"
    )
    session.add_and_upload_new_message(
        {
            "question": "Original question?",
            "csv_data": "test, csv",
            "input_conversation": "Original input conversation.",
            "genesfound": None,
            "variantsFound": None,
            "timing": {
                "question_creation": None,
                "sql_generation": None,
            },
            "full_answer": "This is the full answer <SQL_QUERY/>",
            "sql": "SELECT *;",
        }
    )
