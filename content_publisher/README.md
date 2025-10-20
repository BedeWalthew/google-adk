# Content Publishing System

An advanced multi-agent system demonstrating **nested orchestration** - parallel pipelines within a sequential workflow, with real Google Search integration.

## Overview

This agent showcases the most complex orchestration pattern: **3 sequential pipelines running in parallel**, followed by sequential content creation. It combines parallel research gathering with sequential synthesis, using real Google Search tools.

## Architecture

```
User Topic
     ↓
┌─────────────────────────────────────────────────────────────┐
│              PHASE 1: PARALLEL RESEARCH                     │
│                                                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────┐ │
│  │  News Pipeline   │  │ Social Pipeline  │  │  Expert  │ │
│  │  (Sequential)    │  │  (Sequential)    │  │ Pipeline │ │
│  │                  │  │                  │  │(Sequential)│
│  │ 1. Fetch News    │  │ 1. Monitor Social│  │1. Find   │ │
│  │    ↓             │  │    ↓             │  │  Experts │ │
│  │ 2. Summarize     │  │ 2. Analyze       │  │   ↓      │ │
│  │                  │  │    Sentiment     │  │2. Extract│ │
│  │                  │  │                  │  │  Quotes  │ │
│  └──────────────────┘  └──────────────────┘  └──────────┘ │
└─────────────────────────────────────────────────────────────┘
     ↓              ↓              ↓
     news_summary   social_insights   expert_quotes
                    ↓
┌─────────────────────────────────────────────────────────────┐
│           PHASE 2: SEQUENTIAL CONTENT CREATION              │
│                                                             │
│                    Article Writer                           │
│                         ↓                                   │
│                    Article Editor                           │
│                         ↓                                   │
│                   Article Formatter                         │
└─────────────────────────────────────────────────────────────┘
     ↓
Published Article (Markdown)
```

## What It Does

### Phase 1: Parallel Research (3 pipelines simultaneously)

**News Pipeline:**
1. Fetches current news articles via Google Search
2. Summarizes key takeaways

**Social Pipeline:**
1. Monitors social media trends and discussions
2. Analyzes sentiment and themes

**Expert Pipeline:**
1. Finds expert opinions and credentials
2. Extracts quotable insights

### Phase 2: Sequential Creation

1. **Writer** - Drafts article from all research
2. **Editor** - Improves clarity and impact
3. **Formatter** - Adds markdown formatting for publication

## Usage

```bash
adk web
# Select content_publisher

# Example prompts:
"Write an article about artificial intelligence trends"
"Create content about climate change solutions"
"Publish an article on cryptocurrency regulation"
```

The system will:
- Research news, social media, and expert opinions in parallel
- Synthesize findings into a polished article
- Format for publication with proper markdown

## Key Takeaways

- **Nested Orchestration**: ParallelAgent containing SequentialAgents inside a SequentialAgent
- **Real Tools**: Uses `google_search` tool for actual web research
- **Complex Workflows**: 9 agents working together in coordinated phases
- **State Management**: Data flows through multiple levels (pipeline → parallel → sequential)
- **Efficiency**: 3x faster research phase via parallelization
- **Modular Design**: Each pipeline is independent and reusable

## Tips & Tricks

### Orchestration Strategy
- **Parallel for independence**: Research tasks don't depend on each other
- **Sequential for dependencies**: Writing needs research; editing needs draft
- **Nested for complexity**: Combine patterns for sophisticated workflows

### Performance Optimization
- **3 parallel pipelines** = ~3x faster than sequential research
- Each pipeline is sequential internally (fetch → process)
- Total agents: 9 (3 pipelines × 2 agents + 3 creation agents)

### Real-World Applications
- Replace mock searches with actual API calls
- Add fact-checking agent before publication
- Include SEO optimization agent
- Add social media post generator

### State Flow
```python
# Pipeline outputs become available to next phase
news_pipeline → news_summary
social_pipeline → social_insights  } All available to article_writer
expert_pipeline → expert_quotes

article_writer → draft_article → article_editor
article_editor → edited_article → article_formatter
article_formatter → published_article (final output)
```

### Error Handling
- If one parallel pipeline fails, others continue
- Sequential agents depend on previous outputs
- Use try/catch in production for robustness

## Pattern

```python
# Step 1: Create sequential sub-pipelines
pipeline1 = SequentialAgent(
    sub_agents=[fetch_agent, process_agent],
    description="Pipeline 1"
)

pipeline2 = SequentialAgent(
    sub_agents=[monitor_agent, analyze_agent],
    description="Pipeline 2"
)

pipeline3 = SequentialAgent(
    sub_agents=[find_agent, extract_agent],
    description="Pipeline 3"
)

# Step 2: Run pipelines in parallel
parallel_phase = ParallelAgent(
    sub_agents=[pipeline1, pipeline2, pipeline3]
)

# Step 3: Sequential synthesis
synthesis_agent1 = Agent(
    instruction="Combine: {output1}, {output2}, {output3}",
    output_key="draft"
)

synthesis_agent2 = Agent(
    instruction="Improve: {draft}",
    output_key="final"
)

# Step 4: Combine phases
complete_system = SequentialAgent(
    sub_agents=[
        parallel_phase,      # Parallel research
        synthesis_agent1,    # Synthesize
        synthesis_agent2     # Finalize
    ]
)
```

## When to Use This Pattern

- ✅ Complex workflows with distinct phases
- ✅ Need to gather data from multiple independent sources
- ✅ Each data source requires multi-step processing
- ✅ Final output depends on synthesizing all inputs
- ✅ Performance is critical (parallel = faster)

**Real-World Examples:**
- Content publishing (this agent)
- Market research reports (multiple data sources)
- Due diligence analysis (parallel investigations)
- Competitive intelligence (multi-source research)
- Academic literature review (parallel paper analysis)

## Comparison with Other Patterns

| Pattern | Agents | Structure | Use Case |
|---------|--------|-----------|----------|
| **Single** (hello_agent) | 1 | Flat | Simple queries |
| **Sequential** (blog_pipeline) | 4 | Linear chain | Dependent steps |
| **Parallel** (travel_planner) | 3+1 | Fan-out/gather | Independent tasks |
| **Nested** (content_publisher) | 9 | Parallel pipelines + sequential | Complex multi-phase |

## Performance Analysis

**Sequential Approach (hypothetical):**
```
News: fetch → summarize → 
Social: monitor → analyze → 
Expert: find → extract → 
Write → Edit → Format
= 8 sequential steps × ~5s = ~40s
```

**Nested Parallel Approach (this agent):**
```
[News Pipeline + Social Pipeline + Expert Pipeline] → Write → Edit → Format
= (2 steps × ~5s) + 3 steps × ~5s = ~25s
```

**Speedup: ~40% faster!**

## Advanced: Adding More Pipelines

Easily extend with additional research sources:

```python
# Add video content pipeline
video_pipeline = SequentialAgent(
    sub_agents=[video_finder, video_analyzer]
)

# Add to parallel research
parallel_research = ParallelAgent(
    sub_agents=[
        news_pipeline,
        social_pipeline,
        expert_pipeline,
        video_pipeline  # New!
    ]
)
```

## Tools Used

- **google_search**: Real Google Search integration
- Fetches actual web results
- Enables real-time research
- Can be replaced with other search APIs

## State Variables

| Variable | Source | Used By |
|----------|--------|---------|
| `raw_news` | news_fetcher | news_summarizer |
| `news_summary` | news_summarizer | article_writer |
| `raw_social` | social_monitor | sentiment_analyzer |
| `social_insights` | sentiment_analyzer | article_writer |
| `raw_experts` | expert_finder | quote_extractor |
| `expert_quotes` | quote_extractor | article_writer |
| `draft_article` | article_writer | article_editor |
| `edited_article` | article_editor | article_formatter |
| `published_article` | article_formatter | Final output |

## Key Concepts Demonstrated

1. **Nested Orchestration** - Agents within agents within agents
2. **Phase-Based Workflow** - Clear separation of research vs. creation
3. **Tool Integration** - Real Google Search API usage
4. **State Propagation** - Data flows through multiple orchestration levels
5. **Modular Design** - Each pipeline is self-contained and reusable
6. **Scalability** - Easy to add more research pipelines
