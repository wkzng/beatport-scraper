import requests
import json
import os
from pprint import pprint
import dotenv


def test_post_request(api_url, test_url):
    """
    Test the API using a POST request with JSON body

    Args:
        api_url (str): The API endpoint URL
        test_url (str): The Beatport URL to test

    Returns:
        dict: The response from the API
    """
    payload = {"url": test_url}
    headers = {"Content-Type": "application/json"}

    print(f"POST Request to: {api_url}")
    print(f"Payload: {json.dumps(payload, indent=2)}\n")

    response = requests.post(api_url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    return response.json()



def test_get_request(api_url, test_url):
    """
    Test the API using a GET request with query parameters

    Args:
        api_url (str): The API endpoint URL
        test_url (str): The Beatport URL to test

    Returns:
        dict: The response from the API
    """
    params = {"url": test_url}

    print(f"GET Request to: {api_url}")
    print(f"Query params: {params}\n")

    response = requests.get(api_url, params=params)
    print(f"Status Code: {response.status_code}")
    return response.json()



if __name__ == '__main__':
    # Load environment variables
    dotenv.load_dotenv()

    # Get configuration from environment
    api_url = os.getenv('API_URL')
    test_url = os.getenv('TEST_URL')

    if not api_url:
        print("Error: API_URL not found in .env file")
        exit(1)

    if not test_url:
        print("Error: TEST_URL not found in .env file")
        exit(1)
        

    print("=" * 60)
    print("Testing Beatport API")
    print("=" * 60)
    print(f"API URL: {api_url}")
    print(f"Test URL: {test_url}")
    print("=" * 60)

    # Test POST request
    print("\n[1] Testing POST Request")
    print("-" * 60)
    try:
        result = test_post_request(api_url, test_url)
        print("\nResponse:")
        pprint(result)

        # Display extracted metadata if successful
        if result.get('status') == 200:
            print("\n✓ Success! Extracted metadata:")
            data = result.get('data', {})
            print(f"  Title: {data.get('title')}")
            print(f"  Audio URL: {data.get('audio_url')}")
            print(f"  Image URL: {data.get('image_url')}")
            print(f"  Platform: {data.get('platform')}")
        else:
            print(f"\n✗ Error (status {result.get('status')}): {result.get('message')}")
    except Exception as e:
        print(f"Error: {e}")

    # Test GET request
    print("\n\n[2] Testing GET Request")
    print("-" * 60)
    try:
        result = test_get_request(api_url, test_url)
        print("\nResponse:")
        pprint(result)

        # Display extracted metadata if successful
        if result.get('status') == 200:
            print("\n✓ Success! Extracted metadata:")
            data = result.get('data', {})
            print(f"  Title: {data.get('title')}")
            print(f"  Audio URL: {data.get('audio_url')}")
            print(f"  Image URL: {data.get('image_url')}")
            print(f"  Platform: {data.get('platform')}")
        else:
            print(f"\n✗ Error (status {result.get('status')}): {result.get('message')}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n" + "=" * 60)