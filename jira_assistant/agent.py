"""
Jira Issue Retrieval Assistant - OpenAPI Tools Demonstration

This agent demonstrates how to use OpenAPIToolset to interact with the
Jira API for issue retrieval and management tasks without writing custom tool functions.
"""

from google.adk.agents import Agent
from google.adk.tools.openapi_tool import OpenAPIToolset
from google.adk.tools.openapi_tool.auth.auth_helpers import token_to_scheme_credential
import os
import base64

# ============================================================================
# OPENAPI SPECIFICATION
# ============================================================================

# Jira API OpenAPI Specification (subset for issue management)
# Based on: https://developer.atlassian.com/cloud/jira/platform/rest/v3/
JIRA_API_SPEC = {
    "openapi": "3.0.0",
    "info": {
        "title": "Jira API",
        "description": "Jira REST API for issue retrieval and management operations",
        "version": "3.0.0"
    },
    "servers": [
        {
            "url": "https://{domain}",
            "variables": {
                "domain": {
                    "default": "your-domain.atlassian.net",
                    "description": "Your Jira domain"
                }
            }
        }
    ],
    "components": {
        "securitySchemes": {
            "basicAuth": {
                "type": "http",
                "scheme": "basic",
                "description": "Basic authentication with email and API token"
            }
        }
    },
    "security": [
        {
            "basicAuth": []
        }
    ],
    "paths": {
        "/rest/api/3/project": {
            "get": {
                "operationId": "list_projects",
                "summary": "List all projects",
                "description": "Returns a list of projects visible to the user.",
                "parameters": [
                    {
                        "name": "recent",
                        "in": "query",
                        "description": "Return projects recently accessed by the user",
                        "required": False,
                        "schema": {
                            "type": "integer",
                            "default": 0
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "id": {"type": "string"},
                                            "key": {"type": "string"},
                                            "name": {"type": "string"},
                                            "projectTypeKey": {"type": "string"},
                                            "simplified": {"type": "boolean"},
                                            "style": {"type": "string"},
                                            "isPrivate": {"type": "boolean"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/rest/api/3/search/jql": {
            "get": {
                "operationId": "search_issues",
                "summary": "Search for issues using JQL",
                "description": "Searches for issues using JQL (Jira Query Language).",
                "parameters": [
                    {
                        "name": "jql",
                        "in": "query",
                        "description": "JQL query string",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "startAt",
                        "in": "query",
                        "description": "The index of the first item to return",
                        "required": False,
                        "schema": {
                            "type": "integer",
                            "default": 0
                        }
                    },
                    {
                        "name": "maxResults",
                        "in": "query",
                        "description": "The maximum number of items to return",
                        "required": False,
                        "schema": {
                            "type": "integer",
                            "default": 50
                        }
                    },
                    {
                        "name": "fields",
                        "in": "query",
                        "description": "A comma-separated list of fields to return",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "default": "summary,status,assignee,priority,issuetype"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "startAt": {"type": "integer"},
                                        "maxResults": {"type": "integer"},
                                        "total": {"type": "integer"},
                                        "issues": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {"type": "string"},
                                                    "key": {"type": "string"},
                                                    "fields": {"type": "object"}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "operationId": "search_issues_post",
                "summary": "Search for issues using JQL (POST)",
                "description": "Searches for issues using JQL with POST request (for complex queries).",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "jql": {
                                        "type": "string",
                                        "description": "JQL query string"
                                    },
                                    "startAt": {
                                        "type": "integer",
                                        "description": "The index of the first item to return",
                                        "default": 0
                                    },
                                    "maxResults": {
                                        "type": "integer",
                                        "description": "The maximum number of items to return",
                                        "default": 50
                                    },
                                    "fields": {
                                        "type": "array",
                                        "description": "List of fields to return",
                                        "items": {
                                            "type": "string"
                                        },
                                        "default": ["summary", "status", "assignee", "priority", "issuetype"]
                                    }
                                },
                                "required": ["jql"]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "startAt": {"type": "integer"},
                                        "maxResults": {"type": "integer"},
                                        "total": {"type": "integer"},
                                        "issues": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {"type": "string"},
                                                    "key": {"type": "string"},
                                                    "fields": {"type": "object"}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/rest/api/3/issue/{issueIdOrKey}": {
            "get": {
                "operationId": "get_issue",
                "summary": "Get issue details",
                "description": "Returns the details of an issue.",
                "parameters": [
                    {
                        "name": "issueIdOrKey",
                        "in": "path",
                        "description": "The ID or key of the issue",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "fields",
                        "in": "query",
                        "description": "A comma-separated list of fields to return",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "default": "*all"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "string"},
                                        "key": {"type": "string"},
                                        "fields": {"type": "object"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/rest/api/3/issue": {
            "post": {
                "operationId": "create_issue",
                "summary": "Create issue",
                "description": "Creates an issue or a sub-task.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "fields": {
                                        "type": "object",
                                        "properties": {
                                            "project": {
                                                "type": "object",
                                                "properties": {
                                                    "key": {"type": "string"}
                                                }
                                            },
                                            "summary": {"type": "string"},
                                            "description": {
                                                "type": "object",
                                                "properties": {
                                                    "type": {"type": "string", "default": "doc"},
                                                    "version": {"type": "integer", "default": 1},
                                                    "content": {
                                                        "type": "array",
                                                        "items": {
                                                            "type": "object"
                                                        }
                                                    }
                                                }
                                            },
                                            "issuetype": {
                                                "type": "object",
                                                "properties": {
                                                    "name": {"type": "string"}
                                                }
                                            },
                                            "priority": {
                                                "type": "object",
                                                "properties": {
                                                    "name": {"type": "string"}
                                                }
                                            }
                                        },
                                        "required": ["project", "summary", "issuetype"]
                                    }
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Issue created successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "string"},
                                        "key": {"type": "string"},
                                        "self": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/rest/api/3/issue/{issueIdOrKey}/comment": {
            "get": {
                "operationId": "get_comments",
                "summary": "Get comments",
                "description": "Returns all comments for an issue.",
                "parameters": [
                    {
                        "name": "issueIdOrKey",
                        "in": "path",
                        "description": "The ID or key of the issue",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "startAt",
                        "in": "query",
                        "description": "The index of the first item to return",
                        "required": False,
                        "schema": {
                            "type": "integer",
                            "default": 0
                        }
                    },
                    {
                        "name": "maxResults",
                        "in": "query",
                        "description": "The maximum number of items to return",
                        "required": False,
                        "schema": {
                            "type": "integer",
                            "default": 50
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "startAt": {"type": "integer"},
                                        "maxResults": {"type": "integer"},
                                        "total": {"type": "integer"},
                                        "comments": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {"type": "string"},
                                                    "author": {"type": "object"},
                                                    "body": {"type": "object"},
                                                    "created": {"type": "string"}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "operationId": "add_comment",
                "summary": "Add comment",
                "description": "Adds a comment to an issue.",
                "parameters": [
                    {
                        "name": "issueIdOrKey",
                        "in": "path",
                        "description": "The ID or key of the issue",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "body": {
                                        "type": "object",
                                        "properties": {
                                            "type": {"type": "string", "default": "doc"},
                                            "version": {"type": "integer", "default": 1},
                                            "content": {
                                                "type": "array",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "type": {"type": "string", "default": "paragraph"},
                                                        "content": {
                                                            "type": "array",
                                                            "items": {
                                                                "type": "object",
                                                                "properties": {
                                                                    "type": {"type": "string", "default": "text"},
                                                                    "text": {"type": "string"}
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Comment added successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "string"},
                                        "self": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/rest/api/3/issue/{issueIdOrKey}/transitions": {
            "get": {
                "operationId": "get_transitions",
                "summary": "Get transitions",
                "description": "Returns the transitions available for an issue.",
                "parameters": [
                    {
                        "name": "issueIdOrKey",
                        "in": "path",
                        "description": "The ID or key of the issue",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "transitions": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {"type": "string"},
                                                    "name": {"type": "string"},
                                                    "to": {
                                                        "type": "object",
                                                        "properties": {
                                                            "id": {"type": "string"},
                                                            "name": {"type": "string"}
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "operationId": "do_transition",
                "summary": "Perform transition",
                "description": "Performs an issue transition.",
                "parameters": [
                    {
                        "name": "issueIdOrKey",
                        "in": "path",
                        "description": "The ID or key of the issue",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "transition": {
                                        "type": "object",
                                        "properties": {
                                            "id": {"type": "string"}
                                        }
                                    }
                                },
                                "required": ["transition"]
                            }
                        }
                    }
                },
                "responses": {
                    "204": {
                        "description": "Transition performed successfully"
                    }
                }
            }
        }
    }
}

# ============================================================================
# OPENAPI TOOLSET WITH AUTHENTICATION
# ============================================================================

# Get Jira credentials from environment
jira_email = os.getenv("JIRA_EMAIL")
jira_api_token = os.getenv("JIRA_API_TOKEN")
jira_domain = os.getenv("JIRA_DOMAIN")

if not jira_email or not jira_api_token or not jira_domain:
    print("WARNING: Jira credentials not found in environment variables.")
    print("Please set JIRA_EMAIL, JIRA_API_TOKEN, and JIRA_DOMAIN in your .env file to use this agent.")
    jira_email = "your_email@example.com"
    jira_api_token = "your_api_token"
    jira_domain = "your-domain.atlassian.net"

# Create Basic Auth credentials (email:api_token)
auth_credentials = base64.b64encode(f"{jira_email}:{jira_api_token}".encode()).decode()

# Create authentication scheme and credential using helper function
auth_scheme, auth_credential = token_to_scheme_credential(
    "apikey",                    # Type: use "apikey" for header-based auth
    "header",                    # Location: token goes in header
    "Authorization",             # Key name: the header name
    f"Basic {auth_credentials}"  # Key value: Basic auth with base64 encoded credentials
)

# Update the server URL with the actual domain
JIRA_API_SPEC["servers"][0]["url"] = f"https://{jira_domain}"

# Create OpenAPIToolset with authentication
jira_toolset = OpenAPIToolset(
    spec_dict=JIRA_API_SPEC,
    auth_scheme=auth_scheme,
    auth_credential=auth_credential
)

# ============================================================================
# AGENT DEFINITION
# ============================================================================

root_agent = Agent(
    name="jira_assistant",
    model="gemini-2.0-flash",

    description="""
    Jira issue retrieval assistant that can search for issues, view details,
    create new issues, and manage issue workflows using the Jira API.
    """,

    instruction="""
    You are an expert Jira assistant for issue management!

    CAPABILITIES:
    - List projects in the user's Jira instance
    - Search for issues using JQL (Jira Query Language)
    - Get detailed information about specific issues
    - View issue comments
    - Create new issues
    - Add comments to issues
    - Transition issues through workflows

    WORKFLOW FOR DISCOVERING PROJECTS:
    1. Use list_projects to see available projects
    2. Use search_issues to find issues in a specific project

    WORKFLOW FOR ISSUE MANAGEMENT:
    1. Use search_issues to find relevant issues
    2. Use get_issue to get detailed information about a specific issue
    3. Use get_comments to view issue comments
    4. Use add_comment to add comments to an issue
    5. Use get_transitions to see available workflow transitions
    6. Use do_transition to move an issue through its workflow

    JQL TIPS:
    - Basic format: field operator value
    - Common fields: project, issuetype, status, priority, assignee, reporter, created, updated
    - Common operators: =, !=, >, >=, <, <=, IN, NOT IN, ~ (contains), !~ (does not contain)
    - Examples:
      - project = "PROJECT-KEY" AND status = "Open"
      - issuetype = Bug AND priority IN (High, Highest)
      - assignee = currentUser() AND status != Done
      - created >= -30d AND project = "PROJECT-KEY"

    ISSUE CREATION TIPS:
    - Required fields: project key, summary, issue type
    - Common issue types: Bug, Task, Story, Epic
    - Common priorities: Highest, High, Medium, Low, Lowest

    IMPORTANT NOTES:
    - Always use proper JQL syntax for searches
    - Issue keys are in the format PROJECT-123
    - For complex searches, use search_issues_post instead of search_issues
    - When creating issues or adding comments, follow the Atlassian Document Format
    - Be helpful and explain Jira concepts to users who may be unfamiliar

    EXAMPLE INTERACTIONS:
    - "List all projects in my Jira instance"
    - "Find all open bugs in the PROJECT-123 project"
    - "Show me details for issue PROJECT-456"
    - "Create a new bug in PROJECT-123 with high priority"
    - "Add a comment to issue PROJECT-789 about the latest update"
    - "What transitions are available for issue PROJECT-101?"
    - "Move issue PROJECT-101 to 'In Progress'"
    """,

    # Pass the toolset to the agent
    tools=[jira_toolset]
)
