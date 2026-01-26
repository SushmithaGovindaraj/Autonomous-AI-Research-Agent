from config import get_llm
from state import AgentState
from search_tools import search_query
from langchain_core.messages import HumanMessage, SystemMessage

RESEARCHER_SYSTEM_PROMPT = """
Extract key facts, statistics, and data points from these search results.
Focus on quantitative data, trends, and verifiable information.
Current research step: {current_step}
"""

def researcher_node(state: AgentState):
    print(f"--- [RESEARCHING]: {state['current_step']} ---")
    
    # Perform web search
    query = state['current_step']
    search_results = search_query(query)
    
    if not search_results or len(search_results.strip()) < 100:
        raise Exception(f"Unable to find relevant data for '{query}'. Please try a different query or check your internet connection.")
    
    # Extract and structure the data using Claude
    llm = get_llm()
    messages = [
        SystemMessage(content=RESEARCHER_SYSTEM_PROMPT.format(current_step=state['current_step'])),
        HumanMessage(content=f"Search Results:\n{search_results}")
    ]
    
    response = llm.invoke(messages)
    extracted_data = response.content
    
    # Extract source URLs for transparency
    import re
    source_urls = re.findall(r'Source: (https?://[^\s]+)', search_results)
    
    new_context = state['context'] + "\n\n" + extracted_data
    return {
        "context": new_context,
        "sources": state.get('sources', []) + source_urls[:5],
        "completed_steps": state['completed_steps'] + [state['current_step']]
    }
