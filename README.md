# Google ADK Learning Journey

This repository showcases my learning journey with **Google Agent Development Kit (ADK)** and the various agents I built along the way.

## 🎯 About This Project

This is a collection of AI agents demonstrating different capabilities and patterns using Google's Agent Development Kit. Each agent explores different aspects of the framework, from simple tool usage to complex API integrations.

## 🤖 Agents Built

### 1. **Hello Agent** (`hello_agent/`)
A simple starter agent to understand the basics of Google ADK.
- Basic agent setup
- Simple interactions
- Foundation for learning

### 2. **Chuck Norris Agent** (`chuck_norris_agent/`)
Demonstrates **OpenAPI Tools** integration without writing custom tool functions.
- **Pattern:** OpenAPIToolset with public API
- **API:** Chuck Norris Jokes API
- **Tools:** Random jokes, search, categories
- **Key Learning:** Automatic tool generation from OpenAPI specs

### 3. **Finance Assistant** (`finance_assistant/`)
Shows how to create **custom function tools** for domain-specific calculations.
- **Pattern:** Custom Python function tools
- **Tools:** 
  - Compound interest calculator
  - Loan payment calculator
  - Monthly savings planner
- **Key Learning:** Building specialized tools with validation and error handling

### 4. **GitHub Review Agent** (`github_review_agent/`)
Advanced agent using **authenticated OpenAPI tools** for code review automation.
- **Pattern:** OpenAPIToolset with authentication
- **API:** GitHub REST API
- **Tools:**
  - List repositories
  - List pull requests
  - Get PR details and files
  - Review comments (read/write)
- **Key Learning:** API authentication, complex workflows, real-world automation

### 5. **Jira Assistant** (`jira_assistant/`)
Powerful agent for Jira issue management using **authenticated OpenAPI tools**.
- **Pattern:** OpenAPIToolset with Basic Auth authentication
- **API:** Jira REST API v3
- **Tools:**
  - List projects
  - Search issues with JQL
  - Get issue details
  - Create issues
  - Add comments
  - Transition issues through workflows
- **Key Learning:** Parallel tool execution, Jira API integration, complex query handling

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

## 📚 Key Concepts Learned

### 1. **Agent Basics**
- Agent configuration (name, model, description, instructions)
- Using Gemini models (gemini-2.0-flash, gemini-2.5-flash)
- Instruction engineering for agent behavior

### 2. **Tool Integration Patterns**

**Custom Function Tools:**
```python
def my_tool(param: str) -> dict:
    """Tool description for the LLM"""
    return {"result": "..."}

agent = Agent(tools=[my_tool])
```

**OpenAPI Tools (No Auth):**
```python
toolset = OpenAPIToolset(spec_dict=OPENAPI_SPEC)
agent = Agent(tools=[toolset])
```

**OpenAPI Tools (With Auth):**
```python
auth_scheme, auth_credential = token_to_scheme_credential(
    "apikey", "header", "Authorization", f"Bearer {token}"
)
toolset = OpenAPIToolset(
    spec_dict=SPEC,
    auth_scheme=auth_scheme,
    auth_credential=auth_credential
)
agent = Agent(tools=[toolset])
```

### 3. **Best Practices**
- Clear, detailed agent instructions
- Proper error handling in tools
- Validation of inputs
- Helpful return formats (human-readable + structured data)
- Security considerations (token management, input sanitization)

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


## 🎓 Learning Outcomes

Through building these agents, I learned:

1. ✅ How to structure and configure AI agents
2. ✅ Different patterns for tool integration
3. ✅ Working with OpenAPI specifications
4. ✅ Handling API authentication securely
5. ✅ Building domain-specific tools
6. ✅ Instruction engineering for agent behavior
7. ✅ Real-world automation with GitHub API
8. ✅ Parallel tool execution for efficient API usage

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
