# Required by ADK for proper Python type hints
from __future__ import annotations

# Import the Agent class
from google.adk.agents import Agent

# Define your agent - MUST be named 'root_agent'
root_agent = Agent(
    name="hello_assistant",
    model="gemini-2.0-flash",
    description="A friendly AI assistant for general conversation",
    instruction=(
        "You are a warm and helpful assistant. "
        "Greet users enthusiastically and answer their questions clearly. "
        "Be conversational and friendly!"
    )
)