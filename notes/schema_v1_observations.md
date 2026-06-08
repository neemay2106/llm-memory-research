# Schema v1 Observations
Date: June 11 2025

## Run Summary
Three tasks completed: CSV column averager, web scraper, binary search tree, rate limiter.

## Structural Issues

**Disconnected task_state nodes**: task_state nodes act as isolated timeline 
markers with zero edges in most runs. They need to be connected to the decisions 
they bracket, not just float as timestamps.

**Orphaned nodes**: Critical constraint nodes frequently have no edges — 
e.g. memory and precision constraints in the rate limiter run were identified 
but never connected to any decision. Constraints without edges are useless 
to a continuation agent.

**Illogical closing edges**: Agent invents a closing edge from the final 
task_state back to node_001 with "implements". No closing edge is better 
than a wrong one.

## Edge Semantic Issues

**"implements" used as default**: When the agent can't find a suitable 
relationship type it defaults to "implements". Needs concrete examples 
in the tool description for each relationship type.

**Wrong edge direction**: Constraint nodes are sometimes placed as the 
source of an "implements" edge pointing to a decision. Decisions create 
constraints — not the other way around.

**Recency bias**: Agent connects nodes recorded in the same turn but 
misses cross-turn connections. Fix: add explicit lookback instruction 
in system prompt after every two nodes recorded.

## Missing Node Types

**No artifact/code nodes**: Graph tracks decisions but not outputs. 
A continuation agent can't tell what was actually produced.

**No external_dependency nodes**: Libraries listed as attributes inside 
nodes rather than as first-class graph nodes. Can't map which decisions 
rely on which libraries.

## Schema v2 Changes Needed

1. Add examples to link_nodes tool description for each relationship type
2. Add "follows" relationship type for sequential chronological edges
3. Add "subtask_of" relationship type for hierarchy
4. Add explicit lookback instruction in system prompt
5. Consider artifact node type — decide in Week 2 runs whether it gets populated
6. Clarify task_state nodes must be connected to surrounding decisions

## Fixes for schema V2

| Problem | Fix in Schema v2 |
|----------|------------------|
| `"implements"` used as default | Add one concrete example per relationship type in `link_nodes` description. |
| Recency bias / missed cross-turn edges | Add explicit lookback instruction to system prompt after every two nodes recorded. |
| Illogical closing edges | Add instruction: do not create edges to or from `task_state` nodes except `follows`. |
| Disconnected `task_state` nodes | System prompt: each `task_state` node must link via `follows` to the decision that preceded it. |
| Orphaned constraint nodes | System prompt: every constraint node must have at least one edge before proceeding. |
| No artifact nodes | Add `artifact` node type and `produces` relationship type in `link_nodes`. |
| Missing `follows` relationship | Add `follows` to valid relationship types. |
| Dependencies vague | Make `dependencies` required on decision nodes; add one-line description per library or dependency. |
| Wrong edge direction | Add instruction: decisions create constraints, so edge direction should be `decision → constraint`, not the reverse. |
| Missing resolution tracking | Add instruction: every constraint node must eventually have an incoming `fixes` or `implements` edge. |