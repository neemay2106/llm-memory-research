import anthropic
import os
from dotenv import load_dotenv
os.environ.pop("ANTHROPIC_API_KEY", None)
load_dotenv(override=True)

api_key = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key= api_key)

tools = [
    {
        "name": "record_decision",
        "description": "Records a decision made during a coding task, along with the rationale for why it was made.",
        "input_schema": {
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": "What decision was made"
                },
                "rationale": {
                    "type": "string",
                    "description": "Why this decision was made"
                }
            },
            "required": ["description", "rationale"]
        }
    }
]

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "You are a coding agent. You must use the record_decision tool whenever you make a coding decision. Decide what data structure to use to store a list of users and their login timestamps, then record your decision."}]
)

for block in response.content:
    if block.type == "tool_use":
        print(f"Tool called: {block.name}")
        print(f"Description: {block.input['description']}")
        print(f"Rationale: {block.input['rationale']}")