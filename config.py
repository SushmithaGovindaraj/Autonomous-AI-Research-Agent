import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

load_dotenv()

def get_llm(temperature=0):
    api_key = os.getenv("ANTHROPIC_API_KEY")
    model_name = os.getenv("MODEL_NAME", "claude-3-5-sonnet-latest")
    
    if not api_key:
        raise ValueError("Please set ANTHROPIC_API_KEY in the .env file")
    
    return ChatAnthropic(
        model=model_name,
        anthropic_api_key=api_key,
        temperature=temperature
    )
