from config import get_llm
from state import AgentState
from langchain_core.messages import HumanMessage, SystemMessage

# This is the "self-correction" step. 
# The agent checks its own work to see if it actually answered the user's question.
# If not, it loops back and tries to fix the missing pieces.
EVALUATOR_SYSTEM_PROMPT = """
You are a senior research reviewer. 
Review the completed research and generated files.
If the research goal is met, provide a comprehensive natural-language summary.
If there are missing pieces or errors, provide specific feedback for the next iteration.

Task Goal: {task}
Completed Steps: {completed_steps}
Context: {context}

Return your response in markdown format. 
If finished, start with "FINAL_REPORT:".
If more work is needed, start with "FEEDBACK:".
"""

def evaluator_node(state: AgentState):
    print("--- [SELF-EVALUATION] ---")
    llm = get_llm()
    messages = [
        SystemMessage(content=EVALUATOR_SYSTEM_PROMPT.format(
            task=state['task'],
            completed_steps=state['completed_steps'],
            context=state['context']
        )),
        HumanMessage(content="Evaluate the current results.")
    ]
    
    response = llm.invoke(messages)
    content = response.content
    
    is_complete = "FINAL_REPORT:" in content
    report = content.replace("FINAL_REPORT:", "").strip() if is_complete else ""
    feedback = content.replace("FEEDBACK:", "").strip() if not is_complete else ""
    
    return {
        "report": report,
        "feedback": feedback,
        "is_complete": is_complete
    }
