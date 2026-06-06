# Schema v1 — Decision Graph
**Date:** June 6, 2025

## Node

A node represents a single decision made by the coding agent.

| Field | Type | Description |
|---------|---------|-------------|
| `node_id` | string | Unique identifier |
| `description` | string | What is being changed and where (file, function, module, etc.) |
| `rationale` | string | Why the change was needed and what triggered it |
| `dependencies` | list | Libraries, modules, APIs, functions, or prior decisions this decision relies on |
| `task_state` | string | Overall task status at the time of the decision |
| `timestamp` | string | When the decision was recorded |

---

## Edge

An edge represents a directional relationship between two decisions.

| Field | Type | Description |
|---------|---------|-------------|
| `edge_id` | string | Unique identifier |
| `source_node_id` | string | Node the edge originates from |
| `target_node_id` | string | Node the edge points to |
| `relationship_type` | string | One of: `depends_on`, `was_constrained_by`, `implements`, `abandoned_because_of`, `fixes`, `passes_data_to`, `optimizes` |
| `passed_context` | string | Specific data, assumptions, constraints, or state passed from source to target |

---