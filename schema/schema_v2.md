# Schema v2 — Decision Graph
Date: June 11 2025

## Top-Level Structure

```json
{
  "task_metadata": {
    "current_task": string,
    "completion_pct": float,
    "status": string
  },
  "nodes": [],
  "edges": []
}
```

---

## Node Types

### decision

| Field | Type | Required | Description |
|---------|---------|---------|---------|
| node_id | string | yes | Unique identifier (e.g. node_001) |
| description | string | yes | What is being changed and where |
| rationale | string | yes | Why this decision was made |
| dependencies | array[string] | no | Libraries, functions, prior decisions, or resources relied upon |
| task_state | string | yes | Summary of overall task status at the time of the decision |

---

### constraint

| Field | Type | Required | Description |
|---------|---------|---------|---------|
| node_id | string | yes | Unique identifier (e.g. constraint_001) |
| constraint_type | string | yes | Category of constraint: performance, memory, dependency, security, architectural, other |
| severity | string | yes | Impact level: blocking, high, moderate, informational |
| status | string | yes | Current state: open, mitigated, resolved, wont_fix |
| description | string | yes | Clear statement of the limitation or restriction |
| rationale | string | yes | Technical explanation for why the constraint exists |
| source | string | yes | Origin of the constraint (e.g. user_prompt, environment_limitation, library_conflict) |

---

### artifact

| Field | Type | Required | Description |
|---------|---------|---------|---------|
| node_id | string | yes | Unique identifier (e.g. artifact_001) |
| description | string | yes | What the artifact is |
| type | string | yes | Artifact category such as file, patch, test, model, config, document, dataset, diagram, schema, API, report, notebook |
| output_summary | string | yes | Summary of generated output |
| location | string | yes | Physical or logical location of the artifact |
| produced_by | string | yes | Node ID of the decision that created the artifact |

---

## Edge Schema

| Field | Type | Required | Description |
|---------|---------|---------|---------|
| edge_id | string | yes | Unique identifier (e.g. edge_001) |
| source_node_id | string | yes | Node where the edge originates |
| target_node_id | string | yes | Node where the edge terminates |
| relationship_type | string | yes | Relationship connecting the nodes |
| rationale | string | yes | Technical justification for why the connection exists |
| passed_context | string | no | Specific information, state, data, assumptions, or outputs transferred between nodes |

---

## Valid Relationship Types

### follows

Indicates temporal or logical sequencing. The source node occurs after the target node but does not necessarily depend on it.

---

### produces

The source node generates the target artifact as an output.

---

### was_constrained_by

The source node's implementation, structure, or outcome was shaped by the target constraint.

---

### depends_on

The source node requires the target node to exist, be completed, or remain available in order to function correctly.

---

### implements

The source node is a concrete realization of a specification, interface, design, plan, or abstract concept represented by the target node.

---

### abandoned_because_of

The source node represents an approach, design, or decision that was discarded due to the target node.

---

### fixes

The source node resolves, mitigates, or eliminates an issue represented by the target node.

---

### passes_data_to

The source node produces information that is consumed by the target node during execution, processing, or reasoning.

---

### optimizes

The source node improves performance, maintainability, quality, resource usage, or efficiency of the target node without changing its intended functionality.

---

## Graph Rules

### Node Rules

- Every node must have a globally unique `node_id`.
- Every node must belong to exactly one node type.
- Node IDs must remain stable throughout the graph lifetime.
- Artifacts should only represent outputs that actually exist or were generated.
- Constraints should represent limitations, requirements, assumptions, blockers, or environmental restrictions.
- Decisions should represent a single reasoning step, implementation choice, or design action.

### Edge Rules

- Every edge must have a globally unique `edge_id`.
- Both source and target nodes must exist before an edge is created.
- Edges are directed.
- Relationship semantics must match the relationship type definition.
- Multiple edge types may exist between the same pair of nodes if justified.
- Self-referential edges are discouraged unless explicitly meaningful.

### Artifact Rules

- Every artifact must reference a valid decision through `produced_by`.
- Artifacts should generally have a corresponding `produces` edge from the producing decision.
- Artifact locations should be as specific as possible.
- Artifacts may be consumed by later decisions through `depends_on` or `passes_data_to` relationships.

### Constraint Rules

- Constraints may remain open, become mitigated, be resolved, or be marked wont_fix.
- Constraints should connect to affected decisions through `was_constrained_by`.
- Blocking constraints should generally explain why progress cannot continue.

### Decision Rules

- Decisions should capture intent, not merely actions.
- Rationales should explain why the decision was made, not only what changed.
- Dependencies should identify important inputs used during decision-making.
- Decisions should be linked to prior decisions using `follows` where appropriate.

### Temporal Consistency

- Decision chains should generally form a connected reasoning history.
- Long-running tasks should maintain continuity through `follows` relationships.
- Artifacts and constraints should be connected to the decisions that created or affected them.

---

## Top-Level Graph Object

| Field | Type | Description |
|---------|---------|---------|
| task_metadata.current_task | string | Current task being worked on |
| task_metadata.completion_pct | float | Estimated completion percentage |
| task_metadata.status | string | Current overall task status |
| nodes | array | Collection of all graph nodes |
| edges | array | Collection of all graph edges |