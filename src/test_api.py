import anthropic
import anthropic
import os
from dotenv import load_dotenv
os.environ.pop("ANTHROPIC_API_KEY", None)
load_dotenv(override=True)

api_key = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key= api_key)


message = client.messages.create(
    model="claude-hakiu-4-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Write a Python function that reverses a linked list."}
    ]
)

print(message.content[0].text)