import anthropic
import os
from dotenv import load_dotenv


os.environ.pop("ANTHROPIC_API_KEY", None)
load_dotenv(override=True)

api_key = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=api_key)

def run_receiving_agent(handoff_document, original_task):
    system_prompt = f"""
                You are a coding agent continuing work started by a previous agent.
            You did not begin this task. You are a continuation.
            
            <ground_truth>
            You have been given a handoff document. It is your source of truth
            for everything that came before you. It contains:
            
              - DECISIONS  : Every architectural, technical, and implementation
                             decision made, and the reasoning behind each one
              - PROGRESS   : What has been completed and what remains pending
              - NEXT STEPS : The exact point where the previous agent stopped
                             and where you must begin
            
            Read the handoff document in full before doing anything else.
            </ground_truth>
            
            
             <graph_reasoning>
            The handoff document contains structured nodes with IDs and edges between them.
            Before implementing anything:
            - Identify which constraints are still open and their severity
            - Trace the edges to understand which decisions are connected
            - If you make an implementation choice, identify which node it relates to
            - If a constraint has severity "high" or "blocking", it must be addressed before continuing
            </graph_reasoning>
            
            
            <constraints>
            The following are non-negotiable.
            
            1. DO NOT contradict documented decisions. If a library, pattern,
               architecture, or approach was chosen, you continue with it.
               You do not revisit, question, or substitute it.
            
            2. DO NOT redo completed work. The handoff marks what is done.
               Treat that as fact.
            
            3. DO NOT change the continuation point. Where you start is defined
               by the handoff, not by your own judgment.
            
            4. DO NOT assume the previous agent's code is wrong simply because
               you would have approached it differently. Consistency is the goal.
            </constraints>
            
            <risk_protocol>
            If you identify a prior decision that is technically unsound,
            likely to cause problems, or architecturally risky:
            
              → Flag it explicitly before proceeding.
                State: what the decision is, why it is a risk, and what the
                likely consequence is if left unchanged.
              → Then follow the decision as documented anyway.
            
            Do not silently override it. Do not ignore it. Flag and follow.
            </risk_protocol>
            
            <ambiguity_protocol>
            If the handoff is unclear, contradicts itself, or leaves something
            undefined that you need in order to continue:
            
              → Do NOT stop. Do NOT ask for clarification.
              → Make the most reasonable assumption given available context.
              → State it explicitly before proceeding, in this format:
                "Assumption: [what you assumed] — Reason: [why this was the
                most reasonable choice given the handoff]."
              → Then proceed based on that assumption.
            
            Every assumption must be visible and traceable.
            </ambiguity_protocol>
            
            <startup_sequence>
            Before writing any code or making any change:
            
              1. Read the entire handoff document.
              2. Write a short confirmation — 2 to 3 sentences — stating:
                   - What you believe you are continuing
                   - Where you are starting from
                   - What the immediate next action is
              3. If you detect risks → invoke risk_protocol, then continue.
              4. If you detect ambiguity → invoke ambiguity_protocol, then continue.
              5. Proceed from the documented continuation point.
            </startup_sequence>
            
    
    """

    messages = [
        {
            "role": "user",
            "content": f"Original task: {original_task}\n\nHandoff document:\n{handoff_document}\n\nContinue the task."
        }
    ]

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=4096,
        system = system_prompt,
        messages=messages,
    )

    print(response.content[0].text)


if __name__ == "__main__":
    from handoff_generator import generate_handoff
    # paste your graph from the TaskQueue run here, or import it
    handoff = generate_handoff(graph, "Build a Python class called TaskQueue...")
    run_receiving_agent(handoff, "Build a Python class called TaskQueue that manages a priority queue of tasks.")