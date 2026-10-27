import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://api.cerebras.ai/v1",
    api_key=os.environ.get("CEREBRAS_API_KEY"),
)

# Speed is the reason to use Cerebras. This script measures it two ways:
# the clock on your machine, and the `time_info` the server sends back.
start = time.perf_counter()
first_token_at = None
last_chunk = None

stream = client.chat.completions.create(
    model="qwen-3.8-27b",
    messages=[
        {"role": "user", "content": "Write a 500-word story about a lighthouse keeper."}
    ],
    max_tokens=8192,
    reasoning_effort="none",
    stream=True,
    # Ask for the usage numbers in the last chunk of the stream.
    stream_options={"include_usage": True},
)

for chunk in stream:
    if chunk.choices and chunk.choices[0].delta.content:
        if first_token_at is None:
            first_token_at = time.perf_counter() - start
        print(chunk.choices[0].delta.content, end="", flush=True)
    if chunk.usage:
        last_chunk = chunk

total = time.perf_counter() - start
tokens = last_chunk.usage.completion_tokens

# `time_info` is a Cerebras field, so it lands in `model_extra`.
# It counts only the time on the chip - no network, no queue.
time_info = last_chunk.model_extra["time_info"]

print("\n\n--- Speed: ---")
print(f"completion tokens        : {tokens}")
print(f"time to first token      : {first_token_at:.2f} s")
print(f"total time (your clock)  : {total:.2f} s")
print(f"tokens/s (your clock)    : {tokens / total:.0f}")
print(f"completion_time (server) : {time_info['completion_time']:.2f} s")
print(f"tokens/s (server)        : {tokens / time_info['completion_time']:.0f}")
