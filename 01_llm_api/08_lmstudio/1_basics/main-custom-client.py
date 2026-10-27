import lmstudio as lms
from pprint import pprint

with lms.Client(api_host="localhost:1234") as client:
    model = client.llm.model("google/gemma-4-e4b")

    chat = lms.Chat("You are an AI assistant.")
    chat.add_user_message("Tell me a joke.")

    response = model.respond(chat)

    print("--- Full response: ---")
    pprint(response)
    print("--- Response text: ---")
    print(response.content)
