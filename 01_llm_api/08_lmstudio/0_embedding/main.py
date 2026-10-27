import lmstudio as lms
from pprint import pprint

model = lms.embedding_model("text-embedding-nomic-embed-text-v1.5")

embedding = model.embed("Llamas are members of the camelid family")

print("--- Full response: ---")
pprint(embedding)
