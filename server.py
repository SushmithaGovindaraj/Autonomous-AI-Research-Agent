from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import os
import asyncio
from agent_workflow import create_research_graph

app = FastAPI(title="Autonomous Research Agent API")

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve generated files (charts, CSVs)
DATA_DIR = "research_outputs"
os.makedirs(DATA_DIR, exist_ok=True)
app.mount("/outputs", StaticFiles(directory=DATA_DIR), name="outputs")

# Mount static files for frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

class ResearchRequest(BaseModel):
    task: str

@app.get("/")
async def root():
    return FileResponse("static/index.html")

async def event_generator(task: str):
    """Generator for Server-Sent Events (SSE)"""
    graph = create_research_graph()
    
    initial_state = {
        "task": task,
        "plan": [],
        "completed_steps": [],
        "current_step": "Initializing...",
        "context": "",
        "code": "",
        "files": [],
        "feedback": "",
        "report": "",
        "sources": [],
        "is_complete": False
    }

    try:
        # Stream updates from the graph
        for output in graph.stream(initial_state):
            for node_name, node_output in output.items():
                # Prepare data to send
                data = {
                    "node": node_name,
                    "current_step": node_output.get("current_step", ""),
                    "plan": node_output.get("plan", []),
                    "report": node_output.get("report", ""),
                    "sources": node_output.get("sources", []),
                    "files": node_output.get("files", [])
                }
                yield f"data: {json.dumps(data)}\n\n"
                await asyncio.sleep(0.1) # Small delay to ensure smooth streaming
        
        # Send complete signal
        yield "data: {\"status\": \"complete\"}\n\n"
    except Exception as e:
        print(f"CRITICAL ERROR in event_generator: {str(e)}")
        error_data = {"error": str(e)}
        yield f"data: {json.dumps(error_data)}\n\n"

@app.post("/api/research/stream")
async def stream_research(request: ResearchRequest):
    return StreamingResponse(event_generator(request.task), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
