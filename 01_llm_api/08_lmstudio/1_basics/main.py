import lmstudio as lms

model = lms.llm("google/gemma-4-e4b")

for _ in range(10):
    chat = lms.Chat("You are pirate")
    chat.add_user_message("Tell me a joke.")
    chat.add_assistant_response(
        "Sure! Here’s one for you: Why did the scarecrow win an award? Because he was outstanding in his field! 🌾😄"
    )
    chat.add_user_message("Tell me another one.")

    response = model.respond(chat)

    print("--- Response text: ---")
    print(response.content)
