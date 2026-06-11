import anthropic
import os
from dotenv import load_dotenv


os.environ.pop("ANTHROPIC_API_KEY", None)
load_dotenv(override=True)

api_key = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=api_key)




def handle_tool_call(graph,tool_name, tool_input):
    if tool_name == "record_decision":
        graph["nodes"].append({"type": "decision", **tool_input})
        graph["task_metadata"]["current_task"] = tool_input["description"]
        graph["task_metadata"]["status"] = tool_input["task_state"]
        if "completion_pct" in tool_input:
            graph["task_metadata"]["completion_pct"] = tool_input["completion_pct"]
        print(f"NODE recorded: {tool_input['node_id']} — {tool_input['description'][:60]}")
    elif tool_name == "record_constraint":
        graph["nodes"].append({"type": "constraint", **tool_input})
        print(f"CONSTRAINT recorded: {tool_input['node_id']} — {tool_input['description'][:60]}")
    elif tool_name == "link_nodes":
        graph["edges"].append(tool_input)
        print(
            f"EDGE recorded: {tool_input['source_node_id']} --{tool_input['relationship_type']}--> {tool_input['target_node_id']}")
    elif tool_name == "record_artifact":
        graph["nodes"].append({"type": "artifact", **tool_input})
        print(f"ARTIFACT recorded: {tool_input['node_id']} — {tool_input['description'][:60]}")
    return {"status": "recorded"}


def run_recording_agent(original_task):
        description_for_relationship_type = """follows
        Indicates temporal/logical sequencing — the source node occurs or is decided after the target, with no direct causal dependency. Example: write_unit_tests follows finalize_api_schema.
        produces
        The source node (a decision or process) generates the target node as an output artifact. Example: run_codegen_step produces types.gen.ts.
        was_constrained_by
        The source node's form or outcome was shaped or bounded by the target constraint. Example: use_sqlite was_constrained_by no_external_services_policy.
        depends_on
        The source cannot proceed or function correctly without the target being complete or available. Example: integration_tests depends_on mock_server_setup.
        implements
        The source is a concrete realization of an abstract spec, plan, or interface defined by the target. Example: JWTAuthMiddleware implements auth_spec.
        abandoned_because_of
        The source decision or path was discarded due to the target node (a blocker, constraint, or failure). Example: graphql_approach abandoned_because_of schema_complexity_blocker.
        fixes
        The source artifact or decision resolves a defect or broken state represented by the target. Example: null_guard_patch fixes null_deref_in_parser.
        passes_data_to
        The source node emits data that the target node consumes at runtime or during execution. Example: csv_parser passes_data_to validation_layer.
        optimizes
        The source improves the performance, quality, or resource usage of the target without changing its interface or correctness. Example: composite_index_on_user_id optimizes user_lookup_query
         """

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
                        "dependencies": {"type": "array", "items": {"type": "string"},
                                         "description": "libraries or functions this relies on, with one-line description of what each contributes"},
                        "task_state": {"type": "string", "description": "brief summary of overall status"},
                    },
                    "required": ["node_id", "description", "rationale", "task_state",],
                }
            },
            {
                "name": "record_constraint",
                "description": "Records a constraint discovered during the coding task.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "node_id": {"type": "string", "description": "unique id e.g. node_002"},
                        "constraint_type": {"type": "string",
                                            "enum": ["performance", "memory", "dependency", "security", "architectural",
                                                     "other"]},
                        "severity": {"type": "string", "enum": ["blocking", "high", "moderate", "informational"]},
                        "status": {"type": "string", "enum": ["open", "mitigated", "resolved", "wont_fix"]},
                        "description": {"type": "string", "description": "Clear statement of the limitation"},
                        "rationale": {"type": "string",
                                      "description": "Technical justification for why this constraint exists"},
                        "source": {"type": "string",
                                   "description": "whats the source of the constrain ex user_prompt, environment_limitation, library_conflict"},
                    },
                    "required": ["node_id", "constraint_type", "severity", "status", "description", "rationale", "source"],
                }
            },
            {
                "name": "record_artifact",
                "description": "Records output at a certain decsion during the coding task.",
                "input_schema": {
                    "type": "object",
                    "properties": {

                        "node_id": {"type": "string", "description": "unique id e.g. node_002"},
                        "description": {"type": "string", "description": "what the artifact is"},
                        "artifact_type": {"type": "string",
                                 "description": "type of artifact,eg:File, patch, test, model, config, document, dataset, diagram"},
                        "output_summary": {"type": "string", "description": "summary of generated output"},
                        "location": {"type": "string", "description": "location of the artifact"},
                        "produced_by": {"type": "string", "description": "node_id of the decision that produced this artifact"},
                    },
                    "required": ["node_id", "description", "artifact_type", "output_summary", "location", "produced_by"]
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
                        "relationship_type": {"type": "string", "description": description_for_relationship_type},
                        "rationale": {"type": "string",
                                      "description": "Technical justification for why this connection was made"},
                        "passed_context": {"type": "string",
                                           "description": "specific data or state passed from source to target"}
                    },
                    "required": ["edge_id", "source_node_id", "target_node_id", "relationship_type", "rationale"]
                }
            },
        ]

        graph = {
            "task_metadata": {
                "current_task": "",
                "completion_pct": 0.0,
                "status": ""
            },
            "nodes": [],
            "edges": []
        }



        message = [

                {
                    "role": "user",
                    "content": f"""You are a coding agent. Your job is to complete the coding task below.
                    As you work on the TASK, use your tools to record every decision you make about the code.
                    
                    Do NOT record decisions about the recording system or workflow initialization.
                    Only record decisions directly related to solving the TASK.
                    
                    TASK: {original_task}
                    
                    Rules:
                    - Call record_decision every time you decide something about the code
                    - Call record_constraint every time you discover a limitation or requirement  
                    - Call record_artifact every time you produce a concrete output
                    - Call link_nodes after every two recorded nodes
                    - Use sequential IDs: node_001, node_002, edge_001, edge_002
                    - Every constraint must have at least one edge
                    - Never create an edge without a rationale
                    
                    Do not wait until the end. Record as you go.
                    """
                }

        ]
        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=4096,
            tools=tools,
            tool_choice={"type": "any", "disable_parallel_tool_use": True},
            messages=message,
        )

        turn_count = 0
        while response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    handle_tool_call(graph,block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": '{"status": "recorded"}'
                    })


            message.append({"role": "assistant", "content": response.content})
            message.append({"role": "user", "content": tool_results})

            turn_count += 1
            if turn_count >= 6:
                break

            response = client.messages.create(
                model="claude-haiku-4-5",
                max_tokens=4096,
                tools=tools,
                tool_choice={"type": "auto", "disable_parallel_tool_use": True},
                messages=message,
            )

        import json
        print("\n--- RAW GRAPH ---")
        print(json.dumps(graph, indent=2))
        from handoff_generator import generate_handoff
        return graph,generate_handoff(graph,original_task)