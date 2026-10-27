import os
from openai import OpenAI
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="http://localhost:8888/v1",
    api_key=os.environ.get("UNSLOTH_API_KEY"),
)

# WARNING: Unsloth holds ONE model at a time. This call unloads whatever chat
# model was loaded and loads the embedding model instead. Turn on
# `Settings > API > Model auto-switch` or you get 400 "No model loaded".
response = client.embeddings.create(
    model="second-state/Nomic-embed-text-v1.5-Embedding-GGUF",
    input="Llamas are members of the camelid family",
)

embedding = response.data[0].embedding

print("--- Usage: ---")
pprint(response.usage)
print("--- Vector: ---")
print(f"{len(embedding)} numbers, first 5: {embedding[:5]}")
