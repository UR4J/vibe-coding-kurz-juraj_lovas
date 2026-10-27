import lmstudio as lms

model = lms.llm("google/gemma-4-e4b")

# -----------------------------------------
# Initialize the chat history
chat = lms.Chat("You are an AI assistant.")
# -----------------------------------------

# First user query
chat.add_user_message("Tell me a joke.")

response1 = model.respond(chat)

# Get assistant's response and add it to the history
chat.add_assistant_response(response1.content)

print("--- Response text: ---")
print(response1.content)

chat.add_user_message("Repeat me please the previous joke.")

response2 = model.respond(chat)

# Get assistant's response and add it to the history
chat.add_assistant_response(response2.content)

print("--- Response text: ---")
print(response2.content)
