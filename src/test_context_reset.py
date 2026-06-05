import anthropic
import os
from dotenv import load_dotenv

os.environ.pop("ANTHROPIC_API_KEY", None)
load_dotenv(override=True)

api_key = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key= api_key)

message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    messages = [{"role": "user", "content": "You are a coding agent continuing work on a Flask REST API with JWT authentication. The previous agent implemented a User model, database layer, register/login/profile endpoints, input validation, and an auth service module. Continue by adding a password reset flow."}],
)


print(message.content[0].text)
print("TURN 1:")
print(f"Total tokens so far: {message.usage.input_tokens + message.usage.output_tokens}")