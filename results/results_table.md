# Experiment Results

## Per-Task Results

| Task | Completion (Graph) | Completion (Baseline) | Δ Completion | Contradictions (Graph) | Contradictions (Baseline) | Unsanctioned (Graph) | Unsanctioned (Baseline) |
|------|-------------------|----------------------|-------------|-----------------------|--------------------------|---------------------|------------------------|
| flatten_json | 1.00 | 1.00 | 0.00 | 0 | 0 | 2 | 2 |
| bst | 1.00 | 1.00 | 0.00 | 0 | 0 | 1 | 2 |
| lru_cache | 1.00 | 1.00 | 0.00 | 0 | 0 | 1 | 2 |
| rate_limiter | 1.00 | 1.00 | 0.00 | 0 | 0 | 2 | 2 |
| duplicate_files | 1.00 | 1.00 | 0.00 | 0 | 0 | 2 | 2 |
| log_detector | 0.50 | 0.50 | 0.00 | 1 | 1 | 2 | 2 |
| retry_decorator | 1.00 | 1.00 | 0.00 | 0 | 0 | 1 | 1 |
| context_manager | 1.00 | 1.00 | 0.00 | 0 | 0 | 2 | 2 |
| event_emitter | 1.00 | 1.00 | 0.00 | 0 | 0 | 2 | 3 |
| schema_validator | 1.00 | 1.00 | 0.00 | 0 | 0 | 0 | 2 |

---

## Aggregate Results

| Condition | Avg Completion | Avg Contradictions | Avg Unsanctioned | Success Rate |
|-----------|---------------|-------------------|------------------|-------------|
| Graph Memory | 0.95 | 0.10 | 1.50 | 90% |
| Baseline | 0.95 | 0.10 | 2.00 | 90% |

---

## Metric Definitions

### Completion

Fraction of task requirements successfully implemented.

**Range:** 0.0 – 1.0

Examples:

- 1.0 = Fully completed
- 0.8 = Most requirements completed
- 0.5 = Roughly half completed
- 0.0 = Failed to complete task

### Contradictions

Number of actions or decisions that directly contradict:

- Previous reasoning
- Existing implementation
- Earlier design decisions
- Explicit task requirements

**Lower is better.**

### Unsanctioned Actions

Number of actions taken without support from:

- Retrieved memory
- Existing codebase context
- Prior reasoning trace
- Explicit task instructions

Examples:

- Inventing APIs that do not exist
- Refactoring unrelated code
- Making unsupported assumptions

**Lower is better.**

### Success Rate

Percentage of tasks satisfying:

- Completion ≥ 0.90
- Contradictions = 0

Formula:

```text
Success Rate =
(# successful tasks / total tasks) × 100
```

For this experiment:

```text
Graph Memory:
9 / 10 tasks successful = 90%

Baseline:
9 / 10 tasks successful = 90%
```

---

## Notes

### Graph Condition

Observations:

- Achieved full completion on 9 of 10 tasks and partial completion on the log detector task.
- Produced fewer unsanctioned decisions overall (15 total) than the baseline condition (20 total).
- Demonstrated strong adherence to recorded design decisions, with only one contradiction occurring in the log detector task.

### Baseline Condition

Observations:

- Achieved the same completion and success rate as the graph condition.
- Generated a higher number of unsanctioned decisions (20 total), indicating greater tendency to introduce unsupported implementation details.
- Exhibited the same contradiction pattern as the graph condition on the log detector task.

### Overall Findings

- Graph Memory and Baseline achieved identical completion scores (0.95 average) and contradiction rates (0.10 average).
- Graph Memory reduced unsanctioned decisions by 25% (1.50 vs. 2.00 average per task).
- The primary measurable benefit of the decision graph was improved adherence to previously established decisions rather than higher task completion.
- Both conditions struggled with the same performance-related issue in the log detector task, suggesting the failure was due to task complexity rather than memory retrieval.
- Results indicate that decision-graph memory improves implementation discipline and reduces unsupported elaborations, even when overall task success remains unchanged.

---

## Summary Statistics

| Metric | Graph Memory | Baseline | Relative Change |
|----------|-------------|-----------|----------------|
| Avg Completion | 0.95 | 0.95 | 0% |
| Avg Contradictions | 0.10 | 0.10 | 0% |
| Avg Unsanctioned | 1.50 | 2.00 | -25% |
| Success Rate | 90% | 90% | 0% |

### Key Result

The decision-graph memory system reduced unsupported implementation decisions by **25%** while maintaining identical completion and contradiction rates relative to the baseline condition.