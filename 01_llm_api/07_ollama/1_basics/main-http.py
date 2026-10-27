import json
import requests
from pprint import pprint

data = {"model": "gpt-oss:20b", "prompt": "Tell me a joke.", "stream": False}

response = requests.post("http://localhost:11434/api/generate", data=json.dumps(data))

print("--- Full response: ---")
pprint(response.json())
print("--- Response text: ---")
print(response.json()["response"])
