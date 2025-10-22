"""
GitHub Code Review Assistant - OpenAPI Tools Demonstration

This agent demonstrates how to use OpenAPIToolset to interact with the
GitHub API for code review tasks without writing custom tool functions.
"""

from google.adk.agents import Agent
from google.adk.tools.openapi_tool import OpenAPIToolset
from google.adk.tools.openapi_tool.auth.auth_helpers import token_to_scheme_credential
import os

# ============================================================================
# OPENAPI SPECIFICATION
# ============================================================================

# GitHub API OpenAPI Specification (subset for PR review)
# Based on: https://docs.github.com/en/rest
GITHUB_API_SPEC = {
    "openapi": "3.0.0",
    "info": {
        "title": "GitHub API",
        "description": "GitHub REST API for pull request review operations",
        "version": "2022-11-28"
    },
    "servers": [
        {
            "url": "https://api.github.com"
        }
    ],
    "components": {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "description": "GitHub Personal Access Token"
            }
        }
    },
    "security": [
        {
            "bearerAuth": []
        }
    ],
    "paths": {
        "/repos/{owner}/{repo}/pulls/{pull_number}": {
            "get": {
                "operationId": "get_pull_request",
                "summary": "Get a pull request",
                "description": "Get detailed information about a specific pull request including title, description, state, files changed, and metadata.",
                "parameters": [
                    {
                        "name": "owner",
                        "in": "path",
                        "description": "Repository owner (username or organization)",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "repo",
                        "in": "path",
                        "description": "Repository name",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "pull_number",
                        "in": "path",
                        "description": "Pull request number",
                        "required": True,
                        "schema": {
                            "type": "integer"
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
                                        "number": {"type": "integer"},
                                        "title": {"type": "string"},
                                        "body": {"type": "string"},
                                        "state": {"type": "string"},
                                        "user": {
                                            "type": "object",
                                            "properties": {
                                                "login": {"type": "string"}
                                            }
                                        },
                                        "head": {
                                            "type": "object",
                                            "properties": {
                                                "ref": {"type": "string"},
                                                "sha": {"type": "string"}
                                            }
                                        },
                                        "base": {
                                            "type": "object",
                                            "properties": {
                                                "ref": {"type": "string"}
                                            }
                                        },
                                        "changed_files": {"type": "integer"},
                                        "additions": {"type": "integer"},
                                        "deletions": {"type": "integer"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/repos/{owner}/{repo}/pulls/{pull_number}/comments": {
            "get": {
                "operationId": "list_review_comments",
                "summary": "List review comments on a pull request",
                "description": "Get all review comments (line-specific comments) for a pull request.",
                "parameters": [
                    {
                        "name": "owner",
                        "in": "path",
                        "description": "Repository owner",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "repo",
                        "in": "path",
                        "description": "Repository name",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "pull_number",
                        "in": "path",
                        "description": "Pull request number",
                        "required": True,
                        "schema": {
                            "type": "integer"
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
                                            "id": {"type": "integer"},
                                            "body": {"type": "string"},
                                            "path": {"type": "string"},
                                            "line": {"type": "integer"},
                                            "user": {
                                                "type": "object",
                                                "properties": {
                                                    "login": {"type": "string"}
                                                }
                                            },
                                            "created_at": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "operationId": "create_review_comment",
                "summary": "Create a review comment on a pull request",
                "description": "Add a new review comment to a specific line in a pull request.",
                "parameters": [
                    {
                        "name": "owner",
                        "in": "path",
                        "description": "Repository owner",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "repo",
                        "in": "path",
                        "description": "Repository name",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "pull_number",
                        "in": "path",
                        "description": "Pull request number",
                        "required": True,
                        "schema": {
                            "type": "integer"
                        }
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["body", "commit_id", "path", "line"],
                                "properties": {
                                    "body": {
                                        "type": "string",
                                        "description": "The comment text"
                                    },
                                    "commit_id": {
                                        "type": "string",
                                        "description": "The SHA of the commit to comment on"
                                    },
                                    "path": {
                                        "type": "string",
                                        "description": "The relative path to the file"
                                    },
                                    "line": {
                                        "type": "integer",
                                        "description": "The line number in the diff to comment on"
                                    }
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Comment created successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "integer"},
                                        "body": {"type": "string"},
                                        "path": {"type": "string"},
                                        "line": {"type": "integer"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/repos/{owner}/{repo}/pulls/{pull_number}/files": {
            "get": {
                "operationId": "list_pull_request_files",
                "summary": "List files in a pull request",
                "description": "Get the list of files changed in a pull request with their diffs.",
                "parameters": [
                    {
                        "name": "owner",
                        "in": "path",
                        "description": "Repository owner",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "repo",
                        "in": "path",
                        "description": "Repository name",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "pull_number",
                        "in": "path",
                        "description": "Pull request number",
                        "required": True,
                        "schema": {
                            "type": "integer"
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
                                            "filename": {"type": "string"},
                                            "status": {"type": "string"},
                                            "additions": {"type": "integer"},
                                            "deletions": {"type": "integer"},
                                            "changes": {"type": "integer"},
                                            "patch": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/repos/{owner}/{repo}/issues/{issue_number}/comments": {
            "post": {
                "operationId": "create_issue_comment",
                "summary": "Create a general comment on a pull request",
                "description": "Add a general comment to a pull request (not tied to a specific line).",
                "parameters": [
                    {
                        "name": "owner",
                        "in": "path",
                        "description": "Repository owner",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "repo",
                        "in": "path",
                        "description": "Repository name",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "issue_number",
                        "in": "path",
                        "description": "Pull request number (PRs are issues in GitHub API)",
                        "required": True,
                        "schema": {
                            "type": "integer"
                        }
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["body"],
                                "properties": {
                                    "body": {
                                        "type": "string",
                                        "description": "The comment text"
                                    }
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Comment created successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "integer"},
                                        "body": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/user/repos": {
            "get": {
                "operationId": "list_user_repositories",
                "summary": "List repositories for the authenticated user",
                "description": "Get a list of repositories owned by the authenticated user.",
                "parameters": [
                    {
                        "name": "per_page",
                        "in": "query",
                        "description": "Number of results per page (max 100)",
                        "required": False,
                        "schema": {
                            "type": "integer",
                            "default": 30
                        }
                    },
                    {
                        "name": "page",
                        "in": "query",
                        "description": "Page number of results",
                        "required": False,
                        "schema": {
                            "type": "integer",
                            "default": 1
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
                                            "id": {"type": "integer"},
                                            "name": {"type": "string"},
                                            "full_name": {"type": "string"},
                                            "private": {"type": "boolean"},
                                            "owner": {
                                                "type": "object",
                                                "properties": {
                                                    "login": {"type": "string"}
                                                }
                                            },
                                            "description": {"type": "string"},
                                            "language": {"type": "string"},
                                            "updated_at": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/repos/{owner}/{repo}/pulls": {
            "get": {
                "operationId": "list_pull_requests",
                "summary": "List pull requests in a repository",
                "description": "Get a list of pull requests for a specific repository.",
                "parameters": [
                    {
                        "name": "owner",
                        "in": "path",
                        "description": "Repository owner",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "repo",
                        "in": "path",
                        "description": "Repository name",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "state",
                        "in": "query",
                        "description": "Filter by state (open, closed, all)",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "enum": ["open", "closed", "all"],
                            "default": "open"
                        }
                    },
                    {
                        "name": "per_page",
                        "in": "query",
                        "description": "Number of results per page (max 100)",
                        "required": False,
                        "schema": {
                            "type": "integer",
                            "default": 30
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
                                            "number": {"type": "integer"},
                                            "title": {"type": "string"},
                                            "state": {"type": "string"},
                                            "user": {
                                                "type": "object",
                                                "properties": {
                                                    "login": {"type": "string"}
                                                }
                                            },
                                            "created_at": {"type": "string"},
                                            "updated_at": {"type": "string"},
                                            "head": {
                                                "type": "object",
                                                "properties": {
                                                    "ref": {"type": "string"}
                                                }
                                            },
                                            "base": {
                                                "type": "object",
                                                "properties": {
                                                    "ref": {"type": "string"}
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
}

# ============================================================================
# OPENAPI TOOLSET WITH AUTHENTICATION
# ============================================================================

# Get GitHub token from environment
github_token = os.getenv("GITHUB_TOKEN")

if not github_token:
    print("WARNING: GITHUB_TOKEN not found in environment variables.")
    print("Please set GITHUB_TOKEN in your .env file to use this agent.")
    github_token = ""  # Provide empty string to avoid None errors

# Create authentication scheme and credential using helper function
# GitHub uses Bearer token in the Authorization header
auth_scheme, auth_credential = token_to_scheme_credential(
    "apikey",                    # Type: use "apikey" for header-based auth
    "header",                    # Location: token goes in header
    "Authorization",             # Key name: the header name
    f"Bearer {github_token}"     # Key value: token with Bearer prefix
)

# Create OpenAPIToolset with authentication
# ADK will automatically generate 7 tools:
# - list_user_repositories(per_page: int, page: int) - List user's repositories
# - list_pull_requests(owner: str, repo: str, state: str, per_page: int) - List PRs in a repo
# - get_pull_request(owner: str, repo: str, pull_number: int) - Get PR details
# - list_review_comments(owner: str, repo: str, pull_number: int) - Get review comments
# - create_review_comment(owner: str, repo: str, pull_number: int, body: str, commit_id: str, path: str, line: int) - Add line comment
# - list_pull_request_files(owner: str, repo: str, pull_number: int) - List changed files
# - create_issue_comment(owner: str, repo: str, issue_number: int, body: str) - Add general comment
github_toolset = OpenAPIToolset(
    spec_dict=GITHUB_API_SPEC,
    auth_scheme=auth_scheme,
    auth_credential=auth_credential
)


# mistake in tutorial
# github_toolset = OpenAPIToolset(
#     spec_dict=GITHUB_API_SPEC,
#     auth_config={"type": "bearer", "token": github_token}
# )


# ============================================================================
# AGENT DEFINITION
# ============================================================================

root_agent = Agent(
    name="github_review_agent",
    model="gemini-2.0-flash",

    description="""
    GitHub code review assistant that can analyze pull requests, review code,
    and provide feedback using the GitHub API via OpenAPI tools.
    """,

    instruction="""
    You are an expert code review assistant for GitHub pull requests!

    CAPABILITIES:
    - List repositories for the authenticated user
    - List pull requests in a repository (open, closed, or all)
    - Get PR details (title, description, changes, metadata)
    - List files changed in a PR with diffs
    - View existing review comments
    - Add review comments (line-specific or general)
    - Analyze code for potential issues

    WORKFLOW FOR DISCOVERING WORK:
    1. Use list_user_repositories to see available repositories
    2. Use list_pull_requests to find PRs in a specific repo
    3. Proceed with code review workflow

    WORKFLOW FOR CODE REVIEW:
    1. Use get_pull_request to understand the PR context
    2. Use list_pull_request_files to see what changed
    3. Analyze the code changes for:
       - Security vulnerabilities (SQL injection, XSS, hardcoded secrets, etc.)
       - Code quality issues (complexity, duplication, naming)
       - Best practices violations
       - Performance concerns
       - Missing error handling
       - Documentation needs
    4. Use list_review_comments to see existing feedback
    5. Use create_issue_comment for general PR feedback
    6. Use create_review_comment for line-specific issues (requires commit_id from PR)

    REVIEW STYLE:
    - Be constructive and helpful, not critical
    - Explain WHY something is an issue
    - Suggest specific improvements
    - Acknowledge good practices
    - Prioritize security and correctness over style
    - Use markdown formatting in comments

    SECURITY FOCUS AREAS:
    - Authentication/authorization issues
    - Input validation and sanitization
    - SQL injection, XSS, CSRF vulnerabilities
    - Hardcoded credentials or secrets
    - Insecure dependencies
    - Improper error handling that leaks info
    - Missing rate limiting or access controls

    IMPORTANT NOTES:
    - Repository format: "owner/repo" (e.g., "facebook/react")
    - PR numbers are integers (e.g., 123)
    - For line comments, you need the commit SHA from get_pull_request
    - The patch field in files shows the actual diff
    - Be respectful - you're helping developers improve their code!

    EXAMPLE INTERACTIONS:
    - "Show me my repositories"
    - "List open pull requests in myorg/myrepo"
    - "Summarize the changes in PR #123 in myorg/myrepo"
    - "Review PR #456 in user/project and check for security issues"
    - "What files changed in PR #789?"
    - "Add a comment to PR #111 about the authentication concern"
    """,

    # Pass the toolset to the agent
    tools=[github_toolset]
)
