import lmstudio as lms

model = lms.llm("google/gemma-4-e4b")

# -----------------------------------------
# First query - fresh chat, no history
chat1 = lms.Chat("You are an AI assistant.")
chat1.add_user_message("Tell me a joke.")

response1 = model.respond(chat1)

print("--- Response text: ---")
print(response1.content)

# -----------------------------------------
# Second query - again a fresh chat, the model cannot recall the joke
chat2 = lms.Chat("You are an AI assistant.")
chat2.add_user_message("Repeat me please the previous joke.")

response2 = model.respond(chat2)

print("--- Response text: ---")
print(response2.content)
