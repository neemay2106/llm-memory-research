
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
            if node.get("status", "open") == "open":
                constraint_nodes.append(node)
    return constraint_nodes

def artifact(graph):
    artifact_nodes = []
    nodes = graph["nodes"]
    for node in nodes:
        if node["type"] == "artifact":
            artifact_nodes.append(node)
    return artifact_nodes

def edges(graph):
    edge_list = []
    key_relationship_types = ["was_constrained_by", "abandoned_because_of","fixes"]
    edges = graph["edges"]
    for edge in edges:
        if edge["relationship_type"] in key_relationship_types:
                edge_list.append(edge)
    return edge_list


def generate_handoff(graph,original_task):
    lines = []

    current_task, completion_pct, status = task_state(graph)
    lines.append(f"The given task by the user was left at this: {current_task}")
    lines.append(f"The status of the given task is: {status}")
    lines.append(f"The completion percentage of the given task is: {completion_pct}")

    lines.append("=== CRITICAL DECISIONS ===")

    decision_nodes = dec(graph)
    for x in range(min(3, len(decision_nodes))):
        node = decision_nodes[x]
        lines.append(f"The id of the node is  {node['node_id']}")
        lines.append(f"The decision made was {node['description']}")
        lines.append(f"the rationale behind was {node['rationale']}")
        lines.append(f"the status of the task after decision was made{node['task_state']}")

    lines.append("=== OPEN CONSTRAINTS ===")

    constant_nodes = constraint(graph)
    for x in range(len(constant_nodes)):
        node = constant_nodes[x]
        lines.append(f"The id of the node is  {node['node_id']}")
        lines.append(f"Type of constraint was {node['constraint_type']}")
        lines.append(f"Severity of the constraint is {node['severity']}")
        lines.append(f"The description of constraint was {node['description']}")
        lines.append(f"The rationale of the constraint is {node['rationale']}")
        lines.append(f"The source of constraint is {node['source']}")

    lines.append("=== ALL DECISIONS ===")


    decision_nodes = dec(graph)
    for node in decision_nodes:
        lines.append(f"The id of the node is  {node['node_id']}")
        lines.append(f"The decision made was {node['description']}")
        lines.append(f"the rationale behind was {node['rationale']}")
        lines.append(f"the status of the task after decision was made{node['task_state']}")

    lines.append("=== ARTIFACTS ===")

    artifact_node = artifact(graph)
    for x in range(len(artifact_node)):
        node = artifact_node[x]
        lines.append(f"The id of the node is  {node['node_id']}")
        lines.append(f"Type of artifact was {node['artifact_type']}")
        lines.append(f"The description of artifact was {node['description']}")
        lines.append(f"The routput summary of the artifact is  {node['output_summary']}")
        lines.append(f"The location of artifact is  {node['location']}")

    lines.append("=== KEY EDGES ===")

    edge_list = edges(graph)
    for x in range(len(edge_list)):
        edge = edge_list[x]
        lines.append(f"The id of the edge is  {edge['edge_id']}")
        lines.append(f"{edge['source_node_id']} -----{edge['relationship_type']}------>{edge['target_node_id']}")
        lines.append(f"rationale of the edge is {edge['rationale']}")

    lines.append("=== CRITICAL DECISIONS ===")

    decision_nodes = dec(graph)
    for x in range(min(3, len(decision_nodes))):
        node = decision_nodes[x]
        lines.append(f"The id of the node is  {node['node_id']}")
        lines.append(f"The decision made was {node['description']}")
        lines.append(f"the rationale behind was {node['rationale']}")
        lines.append(f"the status of the task after decision was made{node['task_state']}")

    lines.append("=== ORIGINAL TASK===")
    lines.append(f"The task is {original_task}")

    return "\n".join(lines)

