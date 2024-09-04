import json
import os
import boto3
import requests

# Fetch API endpoint URL from environment variable
API_ENDPOINT = os.environ.get('API_ENDPOINT')

def lambda_handler(event, context):
    # Prepare request data
    request_data = {
        "key1": "value1",
        "key2": "value2"
    }

    # Send POST request to API endpoint
    response = requests.post(API_ENDPOINT, json=request_data)

    # Check if the request was successful
    if response.status_code == 200:
        # Process the response data
        response_data = response.json()
        processed_data = process_response(response_data)

        return {
            'statusCode': 200,
            'body': json.dumps(processed_data)
        }
    else:
        # Handle error case
        error_message = f"Error: {response.status_code} - {response.text}"
        return {
            'statusCode': response.status_code,
            'body': json.dumps({'error': error_message})
        }

def process_response(response_data):
    """
    Function to process the response data from the API endpoint
    """
    # Perform any necessary data processing or transformation here
    processed_data = {
        "result1": response_data["data1"] * 2,
        "result2": response_data["data2"].upper()
    }

    return processed_data
