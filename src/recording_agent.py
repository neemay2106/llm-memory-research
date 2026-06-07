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
        "description": "Records a coding decision made by the agent.",
        "input_schema": {
            "type": "object",
            "properties": {
                "node_id": {"type": "string", "description": "unique id e.g. node_001"},
                "description": {"type": "string", "description": "what is being changed and where"},
                "rationale": {"type": "string", "description": "why this decision was made"},
                "dependencies": {"type": "array", "items": {"type": "string"}, "description": "libraries or functions this relies on"},
                "task_state": {"type": "string", "description": "overall task completion status right now"}
            },
            "required": ["node_id", "description", "rationale", "task_state"]
        }
    },
    {
        "name": "record_constraint",
        "description": "Records a constraint discovered during the coding task.",
        "input_schema": {
            "type": "object",
            "properties": {
                "node_id": {"type": "string", "description": "unique id e.g. node_002"},
                "description": {"type": "string", "description": "what the constraint is"},
                "rationale": {"type": "string", "description": "why this is a constraint"},
                "task_state": {"type": "string", "description": "overall task completion status right now"}
            },
            "required": ["node_id", "description", "rationale", "task_state"]
        }
    },
    {
        "name": "record_task_state",
        "description": "Records the current state of the overall task.",
        "input_schema": {
            "type": "object",
            "properties": {
                "node_id": {"type": "string", "description": "unique id e.g. node_003"},
                "current_task": {"type": "string", "description": "what is being worked on right now"},
                "completion_pct": {"type": "number", "description": "estimated completion 0.0 to 1.0"},
                "task_state": {"type": "string", "description": "brief summary of overall status"}
            },
            "required": ["node_id", "current_task", "completion_pct", "task_state"]
        }
    },
    {
        "name": "link_nodes",
        "description": "Creates a directed edge between two previously recorded nodes.",
        "input_schema": {
            "type": "object",
            "properties": {
                "edge_id": {"type": "string", "description": "unique id e.g. edge_001"},
                "source_node_id": {"type": "string", "description": "node the edge starts from"},
                "target_node_id": {"type": "string", "description": "node the edge points to"},
                "relationship_type": {"type": "string", "description": "one of: depends_on, was_constrained_by, implements, abandoned_because_of, fixes, passes_data_to, optimizes"},
                "passed_context": {"type": "string", "description": "specific data or state passed from source to target"}
            },
            "required": ["edge_id", "source_node_id", "target_node_id", "relationship_type","passed_context"]
        }
    }
]


graph = {"nodes": [], "edges": []}

def handle_tool_call(tool_name, tool_input):
    if tool_name == "record_decision":
        graph["nodes"].append({"type": "decision", **tool_input})
        print(f"NODE recorded: {tool_input['node_id']} — {tool_input['description'][:60]}")
    elif tool_name == "record_constraint":
        graph["nodes"].append({"type": "constraint", **tool_input})
        print(f"CONSTRAINT recorded: {tool_input['node_id']} — {tool_input['description'][:60]}")
    elif tool_name == "record_task_state":
        graph["nodes"].append({"type": "task_state", **tool_input})
        print(f"TASK STATE recorded: {tool_input['completion_pct']*100:.0f}% — {tool_input['current_task'][:60]}")
    elif tool_name == "link_nodes":
        graph["edges"].append(tool_input)
        print(f"EDGE recorded: {tool_input['source_node_id']} --{tool_input['relationship_type']}--> {tool_input['target_node_id']}")
    return {"status": "recorded"}



message = [
        {
            "role": "user",
            "content": """You are a coding agent. As you work, you MUST use your tools to record every decision, constraint, and task state change in real time.
                        Rules:
                        - Call record_decision every time you decide something about the code
                        - Call record_constraint every time you hit a limitation or requirement
                        - Call record_task_state at the start and after each major step
                        - Call link_nodes after recording two related nodes
                        - Use sequential IDs: node_001, node_002, edge_001, edge_002
                        
                        Do not wait until the end. Record as you go.
                        
                        Build a rate limiter class that limits API calls to N requests per minute.
                        
                        """
        }
    ]
response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=4096,
    tools=tools,
    tool_choice={"type": "auto", "disable_parallel_tool_use": True},
    messages= message,
)


while response.stop_reason == "tool_use":
    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            handle_tool_call(block.name, block.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": '{"status": "recorded"}'
            })

    message.append({"role": "assistant", "content": response.content})
    message.append({"role": "user", "content": tool_results})

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=4096,
        tools=tools,
        tool_choice={"type": "auto", "disable_parallel_tool_use": True},
        messages=message,
    )

import json
print("\n--- FULL GRAPH ---")
print(json.dumps(graph, indent=2))