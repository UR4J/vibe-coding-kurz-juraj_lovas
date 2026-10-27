import requests
import os
from pprint import pprint

headers = {
    "Content-Type": "application/json",
}

response = requests.get(
    "https://jari1pl0ahzk0h-8000.proxy.runpod.net/v1/models",
    headers=headers,
)

print("--- Full response: ---")
print(response)
pprint(response.json())
print("--- Response text: ---")
print(response.json())
