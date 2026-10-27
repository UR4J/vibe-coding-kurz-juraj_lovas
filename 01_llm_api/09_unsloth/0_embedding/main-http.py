import os
import json
import requests
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

headers = {
    "Authorization": f"Bearer {os.environ.get('UNSLOTH_API_KEY')}",
    "Content-Type": "application/json",
}

data = {
    "model": "second-state/Nomic-embed-text-v1.5-Embedding-GGUF",
    "input": "Llamas are members of the camelid family",
}

response = requests.post(
    "http://localhost:8888/v1/embeddings",
    headers=headers,
    data=json.dumps(data),
)

embedding = response.json()["data"][0]["embedding"]

print("--- Usage: ---")
pprint(response.json()["usage"])
print("--- Vector: ---")
print(f"{len(embedding)} numbers, first 5: {embedding[:5]}")
