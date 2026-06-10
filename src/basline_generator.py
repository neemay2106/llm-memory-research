
def task_state(graph):
    metadata = graph["task_metadata"]
    return metadata["current_task"],metadata["completion_pct"],metadata["status"]

def dec(graph):
    decision_nodes = []
    nodes = graph["nodes"]
    for node in nodes:
        if node["type"] == "decision":
            decision_nodes.append(node)
    return decision_nodes

def constraint(graph):
    constraint_nodes = []
    nodes = graph["nodes"]
    for node in nodes:
        if node["type"] == "constraint":
            if node["status"] == "open":
                constraint_nodes.append(node)
    return constraint_nodes

def artifact(graph):
    artifact_nodes = []
    nodes = graph["nodes"]
    for node in nodes:
        if node["type"] == "artifact":
            artifact_nodes.append(node)
    return artifact_nodes



def generate_baseline_summary(graph,original_task):
    lines = []
    current_task, completion_pct, status = task_state(graph)
    lines.append(f"the implmentation is {completion_pct} done.The status of the task is {status},the task is left at {current_task}")

    constant_nodes = constraint(graph)
    for x in range(len(constant_nodes)):
        node = constant_nodes[x]
        lines.append(f"CONSTRAINTS: the constraint is {node['description']} and the type of the constraint is {node['constraint_type']}")

    decision_nodes = dec(graph)
    for node in decision_nodes:
        lines.append(f"DECISION: {node['description']} — Reason: {node['rationale']}")
    artifact_node = artifact(graph)
    for x in range(len(artifact_node)):
        node = artifact_node[x]
        lines.append(f"ARTIFACTS:  {node['output_summary']}")
    lines.append(f"The task is {original_task}")

    return "\n".join(lines)

