# Autonomous AI Research Agent

A sophisticated autonomous research system powered by Claude Sonnet 4 and LangGraph that intelligently plans, researches, analyzes, and visualizes information on any topic.

## 🎯 What It Does

This agent autonomously conducts comprehensive research by:
- Creating a custom research strategy for your topic
- Searching multiple data sources (web + Wikipedia)
- Extracting and analyzing key information
- Generating structured datasets (CSV)
- Creating professional visualizations (charts/graphs)
- Synthesizing findings into detailed reports
- Providing source citations for transparency

## 🏗️ Architecture

Built with state-of-the-art AI technologies:
- **LangGraph**: Orchestrates the autonomous multi-step workflow
- **Claude Sonnet 4**: Powers planning, analysis, and code generation
- **FAISS + Sentence Transformers**: Maintains context across research steps
- **Streamlit**: Provides an intuitive web interface

### Workflow
```
User Query → AI Planner → Web Researcher → Data Analyst → Report Generator
```

Each node operates autonomously, making intelligent decisions about how to proceed.

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/autonomous-research-agent.git
cd autonomous-research-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your API key:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

4. Run the application:
```bash
streamlit run ui.py
```

The app will open at `http://localhost:8502`

## 📊 Example Research Topics

- "Analyze the global renewable energy market and key growth drivers"
- "Research quantum computing breakthroughs and commercial applications"
- "Investigate cryptocurrency adoption trends across different regions"
- "Study the impact of AI on healthcare diagnostics"
- "Examine sustainable agriculture innovations and market size"

## 🔧 Configuration

Edit `.env`:
```env
ANTHROPIC_API_KEY=your_key_here
MODEL_NAME=claude-sonnet-4-20250514
```

## 📁 Project Structure

```
autonomous-research-agent/
├── ui.py                    # Streamlit interface
├── agent_workflow.py        # LangGraph orchestration
├── planner.py              # Research planning
├── researcher.py           # Data gathering & extraction
├── coder.py                # Dataset & visualization generation
├── evaluator.py            # Report synthesis
├── search_tools.py         # Hybrid search system
├── memory.py               # Vector memory
├── config.py               # LLM configuration
├── state.py                # Agent state management
└── requirements.txt        # Dependencies
```

## 💡 Key Features

### Autonomous Planning
The AI analyzes your research goal and creates an optimal execution strategy.

### Hybrid Search
Combines DuckDuckGo for current information with Wikipedia for reliable foundational knowledge.

### Source Transparency
Every data point links back to its original source for verification.

### Intelligent Data Processing
Automatically structures unstructured web data into clean CSV datasets.

### Professional Visualizations
Generates publication-ready charts and graphs using matplotlib.

## � How It Works

### 1. Intelligent Planning
Claude analyzes your research goal and creates a strategic 3-step execution plan.

### 2. Multi-Source Research
The agent searches DuckDuckGo for current information and Wikipedia for foundational knowledge, then extracts relevant data points.

### 3. Data Processing
Structures the gathered information into clean, organized CSV datasets ready for analysis.

### 4. Visualization
Generates professional charts and graphs using matplotlib to illustrate key findings.

### 5. Report Generation
Synthesizes all findings into a comprehensive report with source citations.

## 🤝 Contributing

Contributions welcome! Please submit a Pull Request.

## 📄 License

MIT License - Free for commercial and personal use.

## 🙏 Built With

- [LangGraph](https://github.com/langchain-ai/langgraph) - Agent orchestration
- [Anthropic Claude](https://www.anthropic.com/) - AI reasoning
- [Streamlit](https://streamlit.io/) - Web interface
- [FAISS](https://github.com/facebookresearch/faiss) - Vector search

---

**⭐ Star this repo if you find it useful!**
