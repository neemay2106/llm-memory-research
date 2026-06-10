from recording_agent import run_recording_agent
from receiving_agent import run_receiving_agent
from basline_generator import generate_baseline_summary

original_task = """Write a function that takes a directory path and returns all duplicate files based on content hash"""

# Step 1: Run recording agent on the task
graph, handoff = run_recording_agent(original_task)

import json
print("\n--- RAW GRAPH ---")
print(json.dumps(graph, indent=2))

print("\n--- HANDOFF DOCUMENT ---")
print(handoff)

print("\n--- FLAT BASELINE ---")
baseline = generate_baseline_summary(graph, original_task)
print(baseline)


print("\n--- RECEIVING AGENT (ON HANDOFF DOCUMENT)  ---")
run_receiving_agent(handoff, original_task)

print("\n--- RECEIVING AGENT (ON BASELINE SUMMARY) ---")
run_receiving_agent(baseline, original_task)