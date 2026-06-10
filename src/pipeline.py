from recording_agent import run_recording_agent
from receiving_agent import run_receiving_agent
from basline_generator import generate_baseline_summary

original_task = """Implement a simple in-memory cache with get, set, and expiry functionality.."""

# Step 1: Run recording agent on the task
graph, handoff = run_recording_agent(original_task)

print("\n--- HANDOFF DOCUMENT ---")
print(handoff)

print("\n--- FLAT BASELINE ---")
baseline = generate_baseline_summary(graph, original_task)
print(baseline)


print("\n--- RECEIVING AGENT (ON HANDOFF DOCUMENT)  ---")
run_receiving_agent(handoff, original_task)

print("\n--- RECEIVING AGENT (ON BASELINE SUMMARY) ---")
run_receiving_agent(baseline, original_task)