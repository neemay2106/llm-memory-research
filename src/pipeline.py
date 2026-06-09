from recording_agent import run_recording_agent
from receiving_agent import run_receiving_agent

original_task = "Build a Python class called TaskQueue that manages a priority queue of tasks. Each task has a name, priority (1-5), and a callable to execute. The class should support: adding tasks, executing the highest priority task, and listing all pending tasks ordered by priority."

# Step 1: Run recording agent on the task
graph, handoff = run_recording_agent(original_task)

print("\n--- HANDOFF DOCUMENT ---")
print(handoff)

print("\n--- RECEIVING AGENT ---")
run_receiving_agent(handoff, original_task)