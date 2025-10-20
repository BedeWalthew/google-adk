# Blog Creation Pipeline

A multi-agent sequential pipeline that automates blog post creation from research to final publication-ready content.

## Overview

This agent demonstrates **SequentialAgent** - a pattern where multiple agents work together in a specific order, passing information through a shared state.

## Pipeline Flow

```
User Topic → Research → Write → Edit → Format → Final Blog Post
```

### Agents in the Pipeline

1. **Research Agent** - Gathers 5-7 key facts about the topic
2. **Writer Agent** - Creates engaging blog post draft from research
3. **Editor Agent** - Reviews draft and provides feedback
4. **Formatter Agent** - Applies edits and formats as markdown

## Key Features

- **Sequential Execution**: Agents run in strict order
- **State Sharing**: Each agent reads/writes to shared state using `output_key`
- **Template Variables**: Agents reference previous outputs using `{key_name}`
- **Automated Workflow**: Complete blog creation with single prompt

## Usage

```bash
# Start ADK web interface
adk web

# Example prompts:
"Write a blog post about artificial intelligence"
"Create a blog about sustainable living"
"Blog post on the history of coffee"
```

## How It Works

### State Management

Each agent saves its output to the shared state:

```python
research_agent = Agent(
    output_key="research_findings",  # Saves here
    ...
)

writer_agent = Agent(
    instruction="Research: {research_findings}",  # Reads from here
    output_key="draft_post",
    ...
)
```

### Sequential Execution

```python
blog_creation_pipeline = SequentialAgent(
    sub_agents=[
        research_agent,    # Step 1
        writer_agent,      # Step 2 (uses Step 1 output)
        editor_agent,      # Step 3 (uses Step 2 output)
        formatter_agent    # Step 4 (uses Steps 2 & 3)
    ]
)
```

## Example Output

**Input:** "Write a blog post about quantum computing"

**Output:** A complete markdown blog post with:
- Engaging title
- Well-structured paragraphs
- Key facts integrated naturally
- Proper markdown formatting
- Editorial improvements applied

## Key Learning

- **Multi-agent orchestration** with SequentialAgent
- **State management** between agents
- **Template variable substitution** in instructions
- **Pipeline patterns** for complex workflows
- **Agent specialization** (research, write, edit, format)
