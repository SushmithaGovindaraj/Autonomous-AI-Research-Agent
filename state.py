from typing import List, TypedDict, Annotated, Union
import operator

class AgentState(TypedDict):
    # The original task/goal
    task: str
    # The current plan (list of steps)
    plan: List[str]
    # Steps completed so far
    completed_steps: List[str]
    # Current step being worked on
    current_step: str
    # Research findings / extracted data
    context: str
    # Generated code snippets
    code: str
    # Paths to generated files (CSV, PNG)
    files: List[str]
    # Self-evaluation feedback
    feedback: str
    # Final summary/report
    report: str
    # Source URLs for transparency
    sources: List[str]
    # Flags for progress
    is_complete: bool
