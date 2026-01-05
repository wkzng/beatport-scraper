import boto3
import json
from pprint import pprint


def invoke_lambda(function_name:str, payload:dict) -> dict:
    """
    Invoke a Lambda function remotely using boto3

    Args:
        function_name (str): Name or ARN of the Lambda function
        payload (dict): The payload to send to the Lambda function

    Returns:
        dict: The response from the Lambda function
    """
    # Initialize the Lambda client
    lambda_client = boto3.client('lambda')

    # Invoke the Lambda function
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',  # Use 'Event' for async invocation
        Payload=json.dumps(payload)
    )

    # Parse the response
    return json.loads(response['Payload'].read())




if __name__ == '__main__':
    import os
    import dotenv
    dotenv.load_dotenv()

    # Read the event file
    event_file = 'tests/events/beatport.json'
    with open(event_file, 'r') as f:
        event_data = json.load(f)
        test_url = json.loads(event_data['body'])['url']
     
    # Prepare the payload (matching the expected format in handler.py)
    payload = {
        "body": {
            "url": test_url
        }
    }

    # Invoke the Lambda function
    try:
        function_name = os.getenv('FUNCTION_NAME')
        print(f"Invoking Lambda function: {function_name}")
        print(f"With URL: {test_url}\n")

        result = invoke_lambda(function_name, payload)
        print("Response:")
        pprint(result)

    except Exception as e:
        print(f"Error invoking Lambda function: {e}")
