import os
import requests

# Set your OpenAI API key securely
api_key = os.getenv("OPENAI_API_KEY")  # Ensure your OpenAI API key is set as an environment variable

# URL for the models endpoint
url = "https://api.openai.com/v1/models"

# Make a GET request to list models
headers = {
    "Authorization": f"Bearer {api_key}"
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad responses
    models = response.json()

    # Print the list of models
    print("Available Models:")
    for model in models['data']:
        print(model['id'])

except requests.exceptions.RequestException as e:
    print(f"Error retrieving models: {e}")
except KeyError as e:
    print(f"Unexpected response format: {e}")
