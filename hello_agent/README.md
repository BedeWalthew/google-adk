# Hello Agent

The simplest possible agent - a starting point for learning Google ADK basics.

## Overview

This agent demonstrates the fundamental structure of an ADK agent without any tools or complex features.

## What It Does

- Responds to basic conversational prompts
- No external tools or APIs
- Pure LLM-based responses

## Usage

```bash
adk web
# Select hello_agent and start chatting
```

## Key Takeaways

- **Agent Structure**: Learn the basic `Agent()` configuration
- **Model Selection**: Uses `gemini-2.0-flash` for simple conversations
- **Instructions**: How to write clear agent instructions
- **No Tools Needed**: Sometimes a simple conversational agent is all you need

## Tips & Tricks

- Start here if you're new to ADK
- Focus on understanding the agent configuration parameters
- Experiment with different instruction styles
- This is the foundation - all other agents build on this pattern

## Pattern

```python
agent = Agent(
    name="agent_name",
    model="gemini-2.0-flash",
    description="What the agent does",
    instruction="How the agent should behave"
)
```
