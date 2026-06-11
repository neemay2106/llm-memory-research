from recording_agent import run_recording_agent
from receiving_agent import run_receiving_agent
from basline_generator import generate_baseline_summary

tasks = [
    ("log_file_pattern_detector", "Find all log lines matching a regex pattern that occur within an N-second window with at least K matches"),
    ("retry_detector", "Implement a retry decorator with exponential backoff"),
    ("context_manager", "Implement a context manager that times code blocks and produces a per-label summary report"),
    ("event_emitter", "Implement an event emitter with on, emit, and off methods"),
    ("schema_validator", "Implement a CSV schema validator with type coercion and error accumulation"),
]

# for taskname, orig_task in tasks:
#
#
#         original_task = orig_task
#
#         # Step 1: Run recording agent on the task
#         graph, handoff = run_recording_agent(original_task)
#
#         import json
#         print("\n--- RAW GRAPH ---")
#         print(json.dumps(graph, indent=2))
#
#         print("\n--- HANDOFF DOCUMENT ---")
#         print(handoff)
#
#         print("\n--- FLAT BASELINE ---")
#         baseline = generate_baseline_summary(graph, original_task)
#         print(baseline)
#
#         import os
#         os.makedirs("results/task_runs", exist_ok=True)
#
#         task_name = taskname  # change per task
#
#         with open(f"results/task_runs/{task_name}_graph.json", "w") as f:
#             json.dump(graph, f, indent=2)
#
#         with open(f"results/task_runs/{task_name}_handoff.txt", "w") as f:
#             f.write(handoff)
#
#         with open(f"results/task_runs/{task_name}_baseline.txt", "w") as f:
#             f.write(baseline)

# tasks = [
#     ("fatten_json", "Flatten nested JSON keys into single-level dictionary"),
#     ("binary_search_tree", "Implement a binary search tree with insert, search, delete"),
#     ("lru_cache", "Implement an LRU cache with get and put"),
#     ("rate_limiter", "Implement a rate limiter with N requests per minute"),
#     ("duplicate_files", "Write a function that takes a directory path and returns all duplicate files based on content hash"),
# ]
#
for task_name, original_task in tasks:
    print(f"\n{'='*50}")
    print(f"TASK: {task_name}")
    print(f"{'='*50}")

    with open(f"results/task_runs/{task_name}_handoff.txt") as f:
        handoff = f.read()
    with open(f"results/task_runs/{task_name}_baseline.txt") as f:
        baseline = f.read()

    print(f"\n--- RECEIVING AGENT (GRAPH HANDOFF) ---")
    graph_output = run_receiving_agent(handoff, original_task)

    print(f"\n--- RECEIVING AGENT (BASELINE) ---")
    baseline_output = run_receiving_agent(baseline, original_task)

    with open(f"results/task_runs/{task_name}_graph_output.txt", "w") as f:
        f.write(graph_output)
    with open(f"results/task_runs/{task_name}_baseline_output.txt", "w") as f:
        f.write(baseline_output)