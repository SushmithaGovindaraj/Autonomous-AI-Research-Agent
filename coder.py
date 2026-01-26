from config import get_llm
from state import AgentState
from langchain_core.messages import HumanMessage, SystemMessage
import os
import subprocess

DATA_DIR = "research_outputs"
os.makedirs(DATA_DIR, exist_ok=True)

CODER_SYSTEM_PROMPT = """
You are a data analyst and Python developer. 
Generate clean, well-structured Python code to:
1. Create a CSV dataset from the research data
2. Generate a professional visualization (chart/graph)

Save outputs to:
- {data_dir}/dataset.csv
- {data_dir}/chart.png

Use pandas for data handling and matplotlib for visualization.
Return only the Python code block, no explanations.
"""

def coder_node(state: AgentState):
    print(f"--- [CODING]: {state['current_step']} ---")
    llm = get_llm()
    
    prompt = CODER_SYSTEM_PROMPT.format(data_dir=DATA_DIR)
    messages = [
        SystemMessage(content=prompt),
        HumanMessage(content=f"Research Data:\n{state['context']}\n\nCurrent Step: {state['current_step']}")
    ]
    
    response = llm.invoke(messages)
    code = response.content
    
    # Extract code block
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        code = code.split("```")[1].split("```")[0].strip()
    
    # Execute the generated code
    try:
        exec(code, {"__builtins__": __builtins__, "DATA_DIR": DATA_DIR})
        print("✓ Code executed successfully")
    except Exception as e:
        print(f"⚠️ Code execution error: {str(e)}")
        raise Exception(f"Failed to generate outputs: {str(e)}")
    
    return {
        "code": code,
        "files": [f"{DATA_DIR}/dataset.csv", f"{DATA_DIR}/chart.png"],
        "completed_steps": state['completed_steps'] + [state['current_step']]
    }
