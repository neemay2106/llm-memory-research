import anthropic
import anthropic
import os
from dotenv import load_dotenv
os.environ.pop("ANTHROPIC_API_KEY", None)
load_dotenv(override=True)

api_key = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key= api_key)

messages = [{"role": "user", "content": "You are a coding agent building a REST API in Python using Flask. Start by designing the project structure and implementing user authentication with JWT tokens. Think through your design decisions as you go."}]

followups = [
    "Now implement the database layer using SQLite. Make sure it fits with what you already designed.",
    "Add three endpoints: register user, login, and get user profile. Be consistent with your earlier decisions.",
    "Now add input validation and error handling across all endpoints.",
    "Refactor the authentication logic into a separate module. Don't break anything you built earlier.",
    "Add rate limiting to the login endpoint. Be consistent with the error response format you already defined.",
    "Now add a password reset flow with email tokens. Use the same token approach you used for JWT.",
    "Add unit tests for the authentication service. Test the exact methods you implemented earlier.",
]

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=4096,
    messages=messages
)
print("TURN 1:")
print(f"Total tokens so far: {response.usage.input_tokens + response.usage.output_tokens}")
print(response.content[0].text)
messages.append({"role": "assistant", "content": response.content[0].text})

for i, followup in enumerate(followups):
    messages.append({"role": "user", "content": followup})
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        messages=messages
    )
    print(f"\nTURN {i+2}:")
    print(f"Total tokens so far: {response.usage.input_tokens + response.usage.output_tokens}")
    print(response.content[0].text)
    messages.append({"role": "assistant", "content": response.content[0].text})