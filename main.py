import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# API endpoint for obtaining an access token
auth_url = "https://auth.apps.paloaltonetworks.com/oauth2/access_token"

# API endpoints for making requests (replace with endpoints)
api_urls = [
    "https://api.sase.paloaltonetworks.com/sdwan/v2.1/api/profile",
    "https://api.sase.paloaltonetworks.com/config/v1/jobs"
]

# Authentication credentials from environment variables
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
tsg_id = os.getenv("TSG_ID")


# Function to obtain an access token
def get_access_token():
    payload = {
        "grant_type": "client_credentials",
        "scope": f"tsg_id:{tsg_id}"
    }
    response = requests.post(auth_url, data=payload, auth=(client_id, client_secret))
    response.raise_for_status()
    return response.json()["access_token"]


# Function to make API requests and store JSON results in a dictionary
def make_api_requests(access_token):
    results = {}
    headers = {"Authorization": f"Bearer {access_token}"}

    # Make initial request to /sdwan/v2.1/api/profile
    response = requests.get(api_urls[0], headers=headers)
    response.raise_for_status()

    # Make subsequent requests to other endpoints
    for url in api_urls[1:]:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        results[url] = response.json()

    return results


# Function to find common values in the JSON results
def find_common_values(results):
    common_values = set(results[api_urls[1]].keys())
    for url in api_urls[2:]:
        common_values &= set(results[url].keys())
    return common_values


# Main program
def main():
    try:
        access_token = get_access_token()
        print("Access token obtained successfully.")

        results = make_api_requests(access_token)
        print("API requests made successfully.")

        common_values = find_common_values(results)
        print("Common values found:")
        for value in common_values:
            print(value)

    except requests.exceptions.RequestException as e:
        print("Error occurred during API requests:", e)


if __name__ == "__main__":
    main()