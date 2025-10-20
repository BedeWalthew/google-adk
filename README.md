# Google ADK Learning Journey

A collection of AI agents demonstrating different patterns and capabilities using Google's Agent Development Kit (ADK).

## 🤖 Agents Index

Each agent has its own README with detailed documentation, takeaways, and tips & tricks.

| Agent                                            | Pattern               | Description                                        |
| ------------------------------------------------ | --------------------- | -------------------------------------------------- |
| **[hello_agent/](hello_agent/)**                 | Basic Agent           | Starter agent - ADK fundamentals                   |
| **[chuck_norris_agent/](chuck_norris_agent/)**   | OpenAPI (No Auth)     | Public API integration with OpenAPIToolset         |
| **[finance_assistant/](finance_assistant/)**     | Custom Functions      | Domain-specific tools with custom Python functions |
| **[github_review_agent/](github_review_agent/)** | OpenAPI (Bearer Auth) | GitHub API integration for code review             |
| **[jira_assistant/](jira_assistant/)**           | OpenAPI (Basic Auth)  | Jira API integration with parallel execution       |
| **[blog_pipeline/](blog_pipeline/)**             | Multi-Agent System    | Sequential pipeline with state sharing             |

## 🚀 Getting Started

### Prerequisites

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Google ADK
pip install google-adk
```

### Configuration

Create a `.env` file in the root directory:

```bash
# Google API Key (required for all agents)
GOOGLE_API_KEY=your_google_api_key_here

# GitHub Token (required for github_review_agent only)
GITHUB_TOKEN=ghp_your_github_token_here

# Jira credentials (required for jira_assistant only)
JIRA_EMAIL=your_jira_email@example.com
JIRA_API_TOKEN=your_jira_api_token_here
JIRA_DOMAIN=your-domain.atlassian.net
```

### Running Agents

Each agent can be run using the ADK web interface:

```bash
# Start the web UI
adk web

# Then select the agent you want to interact with
```

## 📚 Quick Reference

For detailed patterns, tips, and best practices, see each agent's README.

**Key Patterns:**

- Custom Python functions
- OpenAPI integration (with/without auth)
- Multi-agent orchestration
- Parallel tool execution

## 🛠️ Tech Stack

- **Framework:** Google Agent Development Kit (ADK)
- **LLM:** Google Gemini (2.0-flash, 2.5-flash)
- **APIs:** Chuck Norris API, GitHub REST API, Jira REST API
- **Language:** Python 3.13+
- **Tools:** OpenAPI, REST APIs, Custom Functions

## 📖 Resources

- [ADK Training](https://raphaelmansuy.github.io/adk_training/)
- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [GitHub REST API Docs](https://docs.github.com/en/rest)
- [Jira REST API Docs](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)

## 📁 Project Structure

```
google-adk-tuto/
├── README.md                    # This file
├── .env                         # Environment variables (not in git)
├── .gitignore                   # Git ignore rules
├── hello_agent/                 # Starter agent
├── chuck_norris_agent/          # OpenAPI integration example
│   ├── agent.py
│   └── README.md
├── finance_assistant/           # Custom tools example
│   ├── agent.py
│   └── __init__.py
├── github_review_agent/         # Advanced authenticated API agent
│   ├── agent.py
│   ├── .env.example
│   ├── __init__.py
│   └── README.md
└── jira_assistant/             # Jira issue management agent
    ├── agent.py
    ├── .env.example
    ├── __init__.py
    ├── example.py
    └── README.md
```

## 📝 License

This is a learning project for educational purposes.

---

**Built with ❤️ while learning Google ADK**
