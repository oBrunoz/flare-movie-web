from os import environ
from dotenv import load_dotenv
import requests

load_dotenv()

api_KEY = environ.get('API_KEY')

headers = {
    'Accept': 'application/json',
    'Authorization': api_KEY,
}

response = requests.get(url=environ.get("GET_TRENDING"), headers=headers)

print(api_KEY)
print(response)