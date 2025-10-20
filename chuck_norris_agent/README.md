# Chuck Norris Agent

Learn OpenAPI tool integration with a public API (no authentication required).

## Overview

This agent demonstrates how to use `OpenAPIToolset` to automatically generate tools from an OpenAPI specification without writing custom functions.

## What It Does

- Fetches random Chuck Norris jokes
- Searches jokes by query
- Lists joke categories
- All via auto-generated tools from OpenAPI spec

## Usage

```bash
adk web
# Select chuck_norris_agent

# Example prompts:
"Tell me a random Chuck Norris joke"
"Search for jokes about programming"
"What joke categories are available?"
```

## Key Takeaways

- **OpenAPIToolset**: Automatic tool generation from API specs
- **No Auth**: Working with public APIs is straightforward
- **operationId**: Each endpoint's `operationId` becomes a tool name
- **Zero Custom Code**: No need to write tool functions manually

## Tips & Tricks

- **Finding Specs**: Many public APIs provide OpenAPI/Swagger specs
- **Tool Names**: The `operationId` in the spec becomes the tool name
- **Testing**: Use public APIs first to learn the pattern before adding auth
- **Spec Structure**: Study the spec structure - it's reusable for any API

## Pattern

```python
API_SPEC = {
    "openapi": "3.0.0",
    "paths": {
        "/jokes/random": {
            "get": {
                "operationId": "get_random_joke",  # Becomes tool name
                ...
            }
        }
    }
}

toolset = OpenAPIToolset(spec_dict=API_SPEC)
agent = Agent(tools=[toolset])
```

## When to Use This Pattern

- ✅ Public APIs without authentication
- ✅ Quick prototyping
- ✅ Learning OpenAPI integration
- ✅ APIs with existing OpenAPI specs
