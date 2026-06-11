## Cross-task pattern (Tasks 1-2)

Contradiction rate: low in both conditions. Not a useful differentiator yet.

Real signal: graph handoff agent shows one instance of genuine edge traversal 
per task (constraint → resolution chain). Baseline agent shows zero. But both 
agents treat the handoff primarily as a flat list.

Core problem: edges are included in the handoff document but not being walked. 
The agent reads node content but doesn't follow edge relationships to make 
inferences.

Hypothesis for Week 4: contradiction count may not be the right metric. 
Completeness and depth of engagement with recorded decisions may matter more.

Recording agent should capture language/platform as an explicit decision node. Currently unrecorded



## Pattern across all 10 tasks
Recording agent consistently produces ~4 nodes (2 decisions + 1-2 constraints+ edges) 

before exiting, regardless of task complexity. Graphs capture early 
architectural decisions, not implementation history. Both conditions are 
derived from the same graph per task, so the A/B comparison remains valid — 
but a richer graph might show larger differences. Limitation for discussion.