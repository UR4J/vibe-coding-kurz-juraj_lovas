import lmstudio as lms
from pprint import pprint

model = lms.llm("google/gemma-4-e4b")

image_handle = lms.prepare_image("./test_image.png")

chat = lms.Chat("You are an AI assistant.")
chat.add_user_message("What is in this image?", images=[image_handle])

response = model.respond(chat)

print("--- Full response: ---")
pprint(response)
print("--- Response text: ---")
print(response.content)
