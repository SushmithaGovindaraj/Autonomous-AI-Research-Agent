import streamlit as st
import os
import pandas as pd
from agent_workflow import create_research_graph
from state import AgentState
from dotenv import load_dotenv
import traceback

load_dotenv()

st.set_page_config(page_title="Autonomous Research Agent", page_icon="🔬", layout="wide")

st.title("🔬 Autonomous AI Research Agent")
st.info("🌐 Powered by Claude Sonnet 4 + LangGraph | Real-time web research with source citations")
st.markdown("Enter any research topic and watch the AI autonomously plan, research, analyze, and visualize findings.")

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .stStatus {
        border-radius: 10px;
        border: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

task_input = st.text_area("Research Goal", "Analyze the global artificial intelligence market trends and generate a comprehensive report with data visualizations.", height=100)


if st.button("Kick off Research"):
    if not task_input:
        st.error("Please enter a task.")
    else:
        # Initialize the workflow
        graph = create_research_graph()
        
        # Fresh state for the run
        initial_state = {
            "task": task_input,
            "plan": [],
            "completed_steps": [],
            "current_step": "",
            "context": "",
            "code": "",
            "files": [],
            "feedback": "",
            "report": "",
            "sources": [],
            "is_complete": False
        }
        
        # Real-time dashboard for agent logs
        try:
            with st.status("Agent is working through the plan...", expanded=True) as status:
                log_container = st.container()
                
                final_state = initial_state
                # Using a loop to capture the generator output
                for output in graph.stream(initial_state):
                    for node_name, node_output in output.items():
                        log_container.write(f"### Node: {node_name}")
                        if "plan" in node_output:
                            log_container.write(f"**Current Plan:** {node_output['plan']}")
                        if "current_step" in node_output:
                            log_container.write(f"**Step:** {node_output['current_step']}")
                        if "report" in node_output and node_output["report"]:
                            final_state.update(node_output)
                    
                status.update(label="Tasks Complete!", state="complete", expanded=False)

            # Show the final findings
            st.divider()
            st.header("📋 Research Insights")
            st.markdown(final_state.get("report", "No report generated."))
            
            # Show sources for transparency
            if final_state.get("sources"):
                st.subheader("🔗 Data Sources")
                for i, source in enumerate(final_state["sources"], 1):
                    st.markdown(f"{i}. [{source}]({source})")
            
            # Results columns
            col1, col2 = st.columns(2)
            
            if os.path.exists("research_outputs/dataset.csv"):
                with col1:
                    st.subheader("📊 Collected Data")
                    df = pd.read_csv("research_outputs/dataset.csv")
                    st.dataframe(df)
                    with open("research_outputs/dataset.csv", "rb") as f:
                        st.download_button("Get CSV", f, "dataset.csv")
                        
            if os.path.exists("research_outputs/chart.png"):
                with col2:
                    st.subheader("📈 Visualization")
                    st.image("research_outputs/chart.png")
                    with open("research_outputs/chart.png", "rb") as f:
                        st.download_button("Get Chart", f, "chart.png")

            # Hidden details for the curious
            with st.expander("Peek into the data pipeline"):
                st.subheader("Raw Data & Context")
                st.code(final_state.get("context", ""))
                st.subheader("Generated Python Script")
                st.code(final_state.get("code", ""), language="python")

        except Exception as e:
            st.error(f"⚠️ Agent encountered an error: {str(e)}")
            with st.expander("Show Technical Debug Info"):
                st.code(traceback.format_exc())
            
            st.info("💡 **Tip:** If you see a 402 or 429 error, it means the free model is busy. Try clicking 'Kick off Research' again in 60 seconds.")
