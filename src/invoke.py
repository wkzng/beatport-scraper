import boto3
import json


import boto3
import json


def invoke_lambda_function(lambda_function_name, event):
    """
    Invokes a Lambda function and passes event parameters.
    
    Args:
    lambda_function_name (str): The name of the Lambda function.
    event (dict): The event parameters to pass to the Lambda function.
    
    Returns:
    dict: The response from the Lambda function invocation.
    """
    # Create a Lambda client using boto3
    session = boto3.Session(profile_name="techwills", region_name="us-east-1")
    lambda_client = session.client('lambda')

    # Convert the event parameters to JSON
    event_json = json.dumps(event)
    
    # Invoke the Lambda function
    response = lambda_client.invoke(
        FunctionName=lambda_function_name,
        InvocationType='RequestResponse',
        Payload=event_json
    )
    # Return the response from the Lambda function invocation
    response = json.loads(response['Payload'].read())
    return response



if __name__ =="__main__":
    lambda_function_name = 'aws-techwills-tools-beatport-dev-beatport'
    event = {
        "url":"https://www.beatport.com/track/junin-shane-robinson-remix/7226500"
    }

    response = invoke_lambda_function(lambda_function_name, event)
    print(response)