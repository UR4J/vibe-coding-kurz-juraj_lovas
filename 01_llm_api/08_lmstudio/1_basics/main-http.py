import json
import requests
from pprint import pprint

data = {"model": "google/gemma-4-e4b", "prompt": "Tell me a joke.", "stream": False}

response = requests.post("http://localhost:1234/v1/completions", data=json.dumps(data))

print("--- Full response: ---")
pprint(response.json())
print("--- Response text: ---")
print(response.json()["choices"][0]["text"])
