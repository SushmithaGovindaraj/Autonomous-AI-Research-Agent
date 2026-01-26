from config import get_llm
from state import AgentState
from langchain_core.messages import HumanMessage, SystemMessage
import json

PLANNER_SYSTEM_PROMPT = """
You are an expert research planner. Break down the research task into a clear, actionable 3-step plan:
1. One comprehensive research step to gather data
2. One step to process and visualize the data  
3. One step to synthesize findings into a report

Return the plan as a JSON array of strings.
Example: ["Research global AI market data and trends", "Create dataset and visualization", "Generate comprehensive analysis report"]
"""

def planner_node(state: AgentState):
    print("--- [PLANNING PHASE] ---")
    llm = get_llm()
    messages = [
        SystemMessage(content=PLANNER_SYSTEM_PROMPT),
        HumanMessage(content=f"Research Task: {state['task']}")
    ]
    
    response = llm.invoke(messages)
    try:
        content = response.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        plan = json.loads(content)
    except:
        plan = [line.strip() for line in response.content.split("\n") if len(line.strip()) > 5][:3]

    return {
        "plan": plan,
        "completed_steps": [],
        "current_step": plan[0] if plan else "None"
    }
