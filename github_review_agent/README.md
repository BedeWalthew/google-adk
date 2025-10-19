# GitHub Review Agent

A code review assistant powered by Google ADK that uses the GitHub API to analyze pull requests, review code, and provide feedback.

## Features

This agent can:
- 📚 List repositories for the authenticated user
- 📋 List pull requests in a repository (open, closed, or all)
- 🔍 Get detailed PR information (title, description, changes, metadata)
- 📁 List all files changed in a PR with diffs
- 💬 View existing review comments
- ✍️ Add review comments (both line-specific and general)
- 🛡️ Analyze code for security issues, best practices, and quality concerns

## Setup

### 1. Install Dependencies

```bash
pip install google-adk
```

### 2. Configure GitHub Token

Create a `.env` file in this directory:

```bash
cp .env.example .env
```

Then edit `.env` and add your GitHub Personal Access Token:

```
GITHUB_TOKEN=ghp_your_token_here
```

**To create a GitHub token:**
1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a descriptive name (e.g., "ADK Review Agent")
4. Select scopes:
   - `repo` (for private repositories)
   - OR `public_repo` (for public repositories only)
5. Click "Generate token" and copy it to your `.env` file

### 3. Add Google API Key

If you haven't already, add your Google API key to the `.env` file:

```
GOOGLE_API_KEY=your_google_api_key_here
```

## Usage

### Running the Agent

adk web

### Example Prompts

**List Your Repositories:**
```
"Show me my repositories"
```

**List Pull Requests:**
```
"List open pull requests in myorg/myrepo"
"Show all PRs in user/project"
```

**Get PR Overview:**
```
"Summarize the changes in PR #123 in facebook/react"
```

**Security Review:**
```
"Review PR #456 in myorg/myrepo and check for security issues"
```

**List Changed Files:**
```
"What files changed in PR #789 in user/project?"
```

**View Comments:**
```
"Show me the existing review comments on PR #111"
```

**Add General Comment:**
```
"Add a comment to PR #222 in myorg/myrepo saying 'Great work on the refactoring!'"
```

**Full Code Review:**
```
"Do a complete code review of PR #333 in company/backend-api, focusing on security and performance"
```

## How It Works

This agent uses **OpenAPIToolset** from Google ADK to automatically generate tools from the GitHub REST API specification. No manual tool functions needed!

### Available Tools

The agent has access to these GitHub API operations:

1. **list_user_repositories** - List user's repositories
   - Parameters: `per_page` (optional), `page` (optional)
   
2. **list_pull_requests** - List PRs in a repository
   - Parameters: `owner`, `repo`, `state` (optional: open/closed/all), `per_page` (optional)
   
3. **get_pull_request** - Get PR details
   - Parameters: `owner`, `repo`, `pull_number`
   
4. **list_pull_request_files** - List changed files with diffs
   - Parameters: `owner`, `repo`, `pull_number`
   
5. **list_review_comments** - Get existing review comments
   - Parameters: `owner`, `repo`, `pull_number`
   
6. **create_issue_comment** - Add general PR comment
   - Parameters: `owner`, `repo`, `issue_number`, `body`
   
7. **create_review_comment** - Add line-specific comment
   - Parameters: `owner`, `repo`, `pull_number`, `body`, `commit_id`, `path`, `line`

### Review Focus Areas

The agent is instructed to check for:

**Security:**
- SQL injection, XSS, CSRF vulnerabilities
- Hardcoded credentials or secrets
- Authentication/authorization issues
- Input validation problems
- Insecure dependencies

**Code Quality:**
- Code complexity and duplication
- Naming conventions
- Best practices violations
- Missing error handling
- Documentation needs

**Performance:**
- Inefficient algorithms
- Resource leaks
- Unnecessary computations

## Architecture

```
github_review_agent/
├── agent.py          # Main agent with OpenAPI spec
├── .env.example      # Environment template
└── README.md         # This file
```

The agent follows the same pattern as other ADK agents in this repository:
- Uses `OpenAPIToolset` for automatic tool generation
- Defines GitHub API endpoints in OpenAPI 3.0 format
- Includes authentication via Bearer token
- Provides detailed instructions for code review workflow

## Limitations

- Cannot approve/reject PRs (requires different API endpoint)
- Cannot modify PR files directly
- Line-specific comments require the commit SHA
- Rate limited by GitHub API (5000 requests/hour for authenticated users)

## Tips

1. **Repository Format:** Always use `owner/repo` format (e.g., `facebook/react`)
2. **PR Numbers:** Use integer PR numbers (e.g., `123`, not `#123`)
3. **Batch Requests:** Ask for multiple things at once for efficiency
4. **Context:** Provide context about what you're looking for in the review

## Example Session

```
You: Review PR #42 in mycompany/backend-api for security issues

Agent: I'll analyze PR #42 for security concerns. Let me get the details...

[Agent calls get_pull_request and list_pull_request_files]

Agent: I've reviewed PR #42 "Add user authentication endpoint". Here are the security concerns:

🔴 CRITICAL:
- Line 45 in auth.py: Password is logged in plain text
- Line 78 in auth.py: SQL query uses string concatenation (SQL injection risk)

🟡 WARNINGS:
- Missing rate limiting on login endpoint
- No input validation on email parameter
- JWT secret should be in environment variable

Would you like me to add these as review comments to the PR?
```

## Troubleshooting

**"GITHUB_TOKEN not found"**
- Make sure you created a `.env` file with your token
- Check that the token has the correct scopes

**"404 Not Found"**
- Verify the repository owner/name is correct
- Check that the PR number exists
- Ensure your token has access to the repository

**"403 Forbidden"**
- Your token may lack required permissions
- Check if the repository is private and your token has `repo` scope

## Learn More

- [GitHub REST API Documentation](https://docs.github.com/en/rest)
- [Google ADK Documentation](https://github.com/google/adk)
- [OpenAPI Specification](https://swagger.io/specification/)
