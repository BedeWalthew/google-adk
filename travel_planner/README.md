# Travel Planning System

A multi-agent system demonstrating the **Fan-Out/Gather pattern** with parallel execution and result synthesis.

## Overview

This agent showcases advanced multi-agent orchestration where multiple agents run **in parallel** (fan-out) to gather data quickly, then a single agent **merges** the results (gather) into a cohesive output.

## Architecture

```
User Request
     ↓
┌────────────────────────────────────┐
│   PARALLEL SEARCH (Fan-Out)       │
│                                    │
│  ┌─────────────┐  ┌─────────────┐ │
│  │   Flight    │  │   Hotel     │ │
│  │   Finder    │  │   Finder    │ │
│  └─────────────┘  └─────────────┘ │
│         ┌─────────────┐            │
│         │  Activity   │            │
│         │   Finder    │            │
│         └─────────────┘            │
└────────────────────────────────────┘
     ↓         ↓         ↓
┌────────────────────────────────────┐
│   GATHER & SYNTHESIZE              │
│                                    │
│      Itinerary Builder             │
│   (Merges all results)             │
└────────────────────────────────────┘
     ↓
Complete Travel Itinerary
```

## What It Does

1. **Parallel Search** (3 agents run simultaneously):
   - Flight Finder → Searches flights
   - Hotel Finder → Searches hotels
   - Activity Finder → Finds activities

2. **Sequential Synthesis**:
   - Itinerary Builder → Combines all results into organized plan

## Usage

```bash
adk web
# Select travel_planner

# Example prompts:
"Plan a 5-day trip to Tokyo in March"
"I need a weekend getaway to Paris"
"Create an itinerary for Barcelona, budget-friendly"
```

## Key Takeaways

- **ParallelAgent**: Run multiple agents simultaneously for speed
- **Fan-Out Pattern**: Distribute work across specialized agents
- **Gather Pattern**: Merge parallel results into unified output
- **Performance**: 3x faster than sequential execution
- **State Sharing**: Each parallel agent writes to state, gather agent reads all
- **Nested Agents**: ParallelAgent inside SequentialAgent

## Tips & Tricks

- **When to Use Parallel**: Independent tasks that don't depend on each other
- **Speed Gains**: N parallel agents = ~N times faster
- **State Management**: Each parallel agent needs unique `output_key`
- **Gather Agent**: Reads from multiple state keys using template variables
- **Error Handling**: If one parallel agent fails, others still complete
- **Real APIs**: Replace mock searches with actual API calls (flights, hotels, etc.)

## Pattern

```python
# Step 1: Create specialized agents
agent1 = Agent(output_key="result1", ...)
agent2 = Agent(output_key="result2", ...)
agent3 = Agent(output_key="result3", ...)

# Step 2: Fan-out with ParallelAgent
parallel_phase = ParallelAgent(
    sub_agents=[agent1, agent2, agent3]  # Run simultaneously
)

# Step 3: Gather with synthesis agent
gather_agent = Agent(
    instruction="Combine: {result1}, {result2}, {result3}",
    output_key="final_result"
)

# Step 4: Combine in SequentialAgent
system = SequentialAgent(
    sub_agents=[
        parallel_phase,  # Fan-out
        gather_agent     # Gather
    ]
)
```

## When to Use This Pattern

- ✅ Multiple independent data sources
- ✅ Need to aggregate results from different APIs
- ✅ Speed is important (parallel = faster)
- ✅ Tasks can run independently
- ✅ Need to synthesize diverse information

**Examples:**
- Travel planning (flights + hotels + activities)
- Market research (multiple data sources)
- Competitive analysis (multiple competitors)
- Multi-source news aggregation
- Parallel document processing

## Performance Comparison

**Sequential (blog_pipeline):**
```
Research → Write → Edit → Format
Time: 4 steps × ~5s = ~20s
```

**Fan-Out/Gather (travel_planner):**
```
[Flight + Hotel + Activity] → Merge
Time: 1 step × ~5s + 1 step × ~5s = ~10s
```

**Speedup: 2x faster!**

## Advanced: Adding Real APIs

Replace mock searches with real API calls:

```python
# Add OpenAPIToolset for real flight search
flight_api = OpenAPIToolset(spec_dict=FLIGHT_API_SPEC)
flight_finder = Agent(
    tools=[flight_api],
    output_key="flight_options"
)

# Same for hotels, activities, etc.
```

## Comparison with Other Patterns

| Pattern | Agents | Execution | Use Case |
|---------|--------|-----------|----------|
| **Sequential** (blog_pipeline) | 4 agents | One after another | Dependent steps |
| **Parallel** (travel_planner) | 3 agents | Simultaneous | Independent tasks |
| **Single** (jira_assistant) | 1 agent | Single execution | Simple queries |
