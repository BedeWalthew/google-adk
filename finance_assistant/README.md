# Finance Assistant

Build custom Python function tools for domain-specific calculations.

## Overview

This agent demonstrates how to create custom tools using Python functions instead of OpenAPI specs. Perfect for specialized business logic and calculations.

## What It Does

- **Compound Interest**: Calculate investment growth over time
- **Loan Payments**: Compute monthly payments for mortgages/loans
- **Savings Planning**: Determine monthly savings needed for goals
- **Parallel Execution**: Can run multiple calculations simultaneously

## Usage

```bash
adk web
# Select finance_assistant

# Example prompts:
"Calculate compound interest on $10,000 at 6% for 5 years"
"What's the monthly payment on a $300,000 loan at 4.5% for 30 years?"
"How much do I need to save monthly to reach $50,000 in 3 years?"
"Compare these 3 investment options..." (parallel execution)
```

## Key Takeaways

- **Custom Functions**: Write your own tools as Python functions
- **Type Hints**: Use proper type hints for parameters
- **Docstrings**: The docstring becomes the tool description for the LLM
- **Return Format**: Return both structured data and human-readable text
- **Validation**: Include input validation and error handling
- **Parallel Execution**: Use `gemini-2.5-flash` + instructions for parallel calls

## Tips & Tricks

- **Clear Docstrings**: The LLM reads your docstring to understand the tool
- **Structured Returns**: Return dicts with both data and readable messages
- **Error Handling**: Always validate inputs and return helpful error messages
- **Parallel Instructions**: Tell the agent explicitly to call tools in parallel
- **Domain Expertise**: Custom functions shine for specialized calculations

## Pattern

```python
def my_calculation(param1: float, param2: int) -> dict:
    """
    Clear description of what this tool does.
    
    Args:
        param1: Description of parameter
        param2: Description of parameter
    
    Returns:
        Dict with results and human-readable report
    """
    # Validate inputs
    if param1 <= 0:
        return {"status": "error", "error": "Invalid input"}
    
    # Do calculation
    result = param1 * param2
    
    # Return structured data + readable text
    return {
        "status": "success",
        "result": result,
        "report": f"The result is {result}"
    }

agent = Agent(
    model="gemini-2.5-flash",  # For parallel execution
    tools=[my_calculation, other_tool],
    instruction="When comparing options, call ALL tools in parallel"
)
```

## When to Use This Pattern

- ✅ Domain-specific calculations
- ✅ Complex business logic
- ✅ No external API needed
- ✅ Full control over implementation
- ✅ Need validation and error handling
- ❌ Don't use for simple API calls (use OpenAPIToolset instead)
