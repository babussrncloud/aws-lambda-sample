import json
import os
import urllib3

# Set up the HTTP client
http = urllib3.PoolManager()

# Define the API endpoint URL
API_ENDPOINT = os.environ.get('API_ENDPOINT')

def lambda_handler(event, context):
    try:
        # Get the request data from the event
        request_data = event.get('body', {})

        # Parse the request data if it's a JSON string
        if isinstance(request_data, str):
            request_data = json.loads(request_data)

        # Make the API request with the request data
        response = http.request('POST', API_ENDPOINT, body=json.dumps(request_data).encode('utf-8'))

        # Check if the request was successful
        if response.status == 200:
            # Parse the response data
            data = json.loads(response.data)

            # Process the response data
            processed_data = process_data(data, request_data)

            # Return the processed data
            return {
                'statusCode': 200,
                'body': json.dumps(processed_data)
            }
        else:
            # Return an error message
            return {
                'statusCode': response.status,
                'body': json.dumps({'error': 'Failed to fetch data from API'})
            }
    except Exception as e:
        # Return an error message for any exceptions
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def process_data(response_data, request_data):
    # Assuming the API response is a list of dictionaries
    processed_data = []

    for item in response_data:
        # Check if the item has a 'name' key
        if 'name' in item:
            name = item['name']
        else:
            name = 'Unknown'

        # Check if the item has an 'age' key and convert it to an integer
        if 'age' in item:
            try:
                age = int(item['age'])
            except ValueError:
                age = 0
        else:
            age = 0

        # Calculate the year of birth based on the age
        import datetime
        current_year = datetime.datetime.now().year
        year_of_birth = current_year - age

        # Add request data to the processed item
        processed_item = {
            'name': name,
            'age': age,
            'year_of_birth': year_of_birth,
            'request_data': request_data
        }

        processed_data.append(processed_item)

    return processed_data
