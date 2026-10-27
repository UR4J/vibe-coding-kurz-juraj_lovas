from ollama import chat
from ollama import ChatResponse
from pprint import pprint

for _ in range(10):
    response: ChatResponse = chat(
        model="gpt-oss:20b",
        messages=[
            {
                "role": "system",
                "content": "You are pirate",
            },
            {"role": "user", "content": "Tell me a joke."},
            {
                "role": "assistant",
                "content": "Sure! Here’s one for you: Why did the scarecrow win an award? Because he was outstanding in his field! 🌾😄",
            },
            {"role": "user", "content": "Tell me another one."},
        ],
    )

    # print("--- Full response: ---")
    # pprint(response)
    print("--- Response text: ---")
    print(response.message.content)
