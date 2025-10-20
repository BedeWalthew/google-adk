# Jira Issue Retrieval Assistant

This agent demonstrates how to use OpenAPIToolset to interact with the Jira API for issue retrieval and management tasks without writing custom tool functions.

## Features

- List projects in your Jira instance
- Search for issues using JQL (Jira Query Language)
- Get detailed information about specific issues
- View issue comments and attachments
- Create and update issues
- Add comments to issues
- Transition issues through workflows

## Setup

1. Create a `.env` file based on `.env.example`
2. Add your Jira credentials:
   - `JIRA_EMAIL`: Your Atlassian account email
   - `JIRA_API_TOKEN`: Create an API token at https://id.atlassian.com/manage-profile/security/api-tokens
   - `JIRA_DOMAIN`: Your Jira domain (e.g., `your-domain.atlassian.net`)
3. Add your Google ADK API key if needed

## Usage

```python
from jira_assistant.agent import root_agent

# Run the agent
response = root_agent.run("Find all open bugs in the PROJECT-123 project")
print(response)
```

## Example Interactions

- "List all projects in my Jira instance"
- "Find all open bugs in the PROJECT-123 project"
- "Show me details for issue PROJECT-456"
- "Create a new bug in PROJECT-123 with high priority"
- "Add a comment to issue PROJECT-789 about the latest update"
- "Transition issue PROJECT-101 to 'In Progress'"
