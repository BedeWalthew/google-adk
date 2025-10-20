# Notes to Self - Google ADK Learning Journey

## 🤖 Agent Analysis - What Makes Each Unique

### 1. Hello Agent (`hello_agent/`)

**Purpose:** Starter agent to understand ADK basics

**What It Uses:**

- Basic Agent configuration
- No tools
- Simple instruction-based responses

**Why It's Unique:**

- Simplest possible agent
- Pure LLM responses without any tools
- Foundation for understanding agent structure

**TL;DR:** Bare-bones agent, no tools, just conversations

---

### 2. Chuck Norris Agent (`chuck_norris_agent/`)

**Purpose:** Learn OpenAPIToolset with a public API (no auth)

**What It Uses:**

- `OpenAPIToolset` with public API
- No authentication required
- Chuck Norris Jokes API

**Why It's Unique:**

- First introduction to OpenAPIToolset
- Shows how to work with public APIs
- No auth complexity - focus on tool generation

**Key Pattern:**

```python
toolset = OpenAPIToolset(spec_dict=OPENAPI_SPEC)
agent = Agent(tools=[toolset])
```

**TL;DR:** OpenAPI tools without authentication - simplest API integration

---

### 3. Finance Assistant (`finance_assistant/`)

**Purpose:** Learn custom Python function tools

**What It Uses:**

- Custom Python functions as tools
- `gemini-2.5-flash` model
- Domain-specific calculations

**Why It's Unique:**

- Only agent using custom Python functions (not OpenAPI)
- Shows how to build specialized tools from scratch
- Demonstrates parallel tool execution
- Includes validation and error handling

**Key Pattern:**

```python
def calculate_compound_interest(principal: float, rate: float) -> dict:
    """Tool description for LLM"""
    # Custom logic here
    return {"result": ...}

agent = Agent(tools=[calculate_compound_interest, ...])
```

**Tools:**

1. `calculate_compound_interest` - Investment growth
2. `calculate_loan_payment` - Loan amortization
3. `calculate_monthly_savings` - Savings planning

**Parallel Execution:**

- Instructions tell agent to call multiple tools simultaneously
- Example: "Compare 3 investment options" → 3 parallel tool calls

**TL;DR:** Custom Python functions as tools, parallel execution, domain expertise

---

### 4. GitHub Review Agent (`github_review_agent/`)

**Purpose:** Learn authenticated OpenAPI tools with Bearer token

**What It Uses:**

- `OpenAPIToolset` with authentication
- Bearer token authentication (GitHub PAT)
- `gemini-2.0-flash` model
- GitHub REST API

**Why It's Unique:**

- First agent with API authentication
- Shows Bearer token pattern
- Complex workflow (PR review process)
- Real-world automation use case

**Authentication Pattern:**

```python
auth_scheme, auth_credential = token_to_scheme_credential(
    "apikey",                    # Type
    "header",                    # Location
    "Authorization",             # Header name
    f"Bearer {github_token}"     # Token with Bearer prefix
)

toolset = OpenAPIToolset(
    spec_dict=GITHUB_API_SPEC,
    auth_scheme=auth_scheme,
    auth_credential=auth_credential
)
```

**Tools Generated:**

- `list_user_repositories` - List repos
- `list_pull_requests` - List PRs
- `get_pull_request` - PR details
- `list_review_comments` - View comments
- `create_review_comment` - Add line comments
- `list_pull_request_files` - View changed files
- `create_issue_comment` - Add general comments

**TL;DR:** Bearer token auth, GitHub API, code review automation

---

### 5. Jira Assistant (`jira_assistant/`)

**Purpose:** Learn Basic Auth and parallel API tool execution

**What It Uses:**

- `OpenAPIToolset` with Basic Authentication
- Base64 encoded email:token
- `gemini-2.5-flash` model (for parallel execution)
- Jira REST API v3

**Why It's Unique:**

- Uses Basic Auth (different from Bearer token)
- Updated to use new Jira API endpoint (`/rest/api/3/search/jql`)
- Explicit parallel execution instructions
- Complex nested object structures (Atlassian Document Format)

**Authentication Pattern:**

```python
# Create Basic Auth credentials
auth_credentials = base64.b64encode(
    f"{jira_email}:{jira_api_token}".encode()
).decode()

auth_scheme, auth_credential = token_to_scheme_credential(
    "apikey",
    "header",
    "Authorization",
    f"Basic {auth_credentials}"  # Basic prefix instead of Bearer
)
```

**Tools Generated:**

- `list_projects` - List all projects
- `search_issues` - JQL search (GET)
- `search_issues_post` - JQL search (POST for complex queries)
- `get_issue` - Issue details
- `create_issue` - Create new issue
- `get_comments` - View comments
- `add_comment` - Add comment
- `get_transitions` - Available workflow transitions
- `do_transition` - Move issue through workflow

**Parallel Execution Instructions:**

```python
instruction = """
PARALLEL EXECUTION:
When users ask about multiple issues or operations, execute ALL
necessary API calls in parallel to be efficient.
"""
```

**API Migration Note:**

- Old endpoint: `/rest/api/3/search` (deprecated)
- New endpoint: `/rest/api/3/search/jql` (current)
- Migration guide: https://developer.atlassian.com/changelog/#CHANGE-2046

**TL;DR:** Basic Auth, parallel execution, Jira API, complex nested objects

---

## 📝 OpenAPI Specification Deep Dive

### Understanding OpenAPI Specs for ADK Tools

**TL;DR:** OpenAPI specs are JSON/dict structures that describe REST APIs. ADK automatically converts each `operationId` into a callable tool.

#### Key Components of an OpenAPI Spec

1. **Basic Info**

   ```python
   {
       "openapi": "3.0.0",
       "info": {"title": "API Name", "version": "1.0.0"}
   }
   ```

2. **Servers** - Where the API lives

   ```python
   "servers": [{"url": "https://api.example.com"}]
   ```

3. **Security** - How to authenticate

   ```python
   "components": {
       "securitySchemes": {
           "basicAuth": {"type": "http", "scheme": "basic"}
       }
   }
   ```

4. **Paths** - The actual endpoints (becomes tools)
   ```python
   "paths": {
       "/endpoint": {
           "get": {
               "operationId": "tool_name",  # This becomes the tool name!
               "parameters": [...],
               "responses": {...}
           }
       }
   }
   ```

### The `security: [{"basicAuth": []}]` Syntax

**Question:** Why the nested arrays in security definitions?

**Answer:**

- **Outer array `[]`**: Defines multiple auth OPTIONS (OR logic)
  - `[{"basicAuth": []}, {"apiKey": []}]` = Use basic auth OR API key
- **Inner array `[]`**: Defines required SCOPES for that auth method
  - Empty `[]` for Basic/Bearer auth (no scopes)
  - `["read:repo", "write:repo"]` for OAuth2 (specific permissions)

**TL;DR:**

- Basic/Bearer auth: Always `{"authName": []}`
- OAuth2: `{"oauth2": ["scope1", "scope2"]}`
- Multiple options: `[{auth1: []}, {auth2: []}]`

### The Two Types of `required`

**Question:** Why `requestBody.required: True` AND `schema.required: ["fields"]`?

**Answer:** They operate at different levels:

1. **`requestBody.required: True`** (Request Body Level)

   - "Must you send ANY body at all?"
   - `True` = Body is mandatory
   - `False` = Body is optional

2. **`schema.required: ["field1", "field2"]`** (Schema Level)
   - "IF you send a body, which fields inside are mandatory?"
   - Validates the structure of the JSON

**Example:**

```python
"requestBody": {
    "required": True,  # MUST send a body
    "content": {
        "application/json": {
            "schema": {
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"}
                },
                "required": ["name"]  # name is mandatory, age is optional
            }
        }
    }
}
```

**TL;DR:** First `required` = "send body?", Second `required` = "which fields inside?"

### Parameter Locations (`in` field)

- **`query`**: URL parameters `?key=value`
- **`path`**: Part of URL `/users/{userId}`
- **`header`**: HTTP headers
- **`cookie`**: Cookie values

### Common Mistakes to Avoid

❌ **WRONG:**

```python
"properties": {
    "jql": {"type": "string", "required": True}  # Don't do this!
}
```

✅ **CORRECT:**

```python
"properties": {
    "jql": {"type": "string"}
},
"required": ["jql"]  # Put required at schema level
```

---

## 🔑 Key Patterns Comparison

### Authentication Methods

| Agent        | Auth Type    | Pattern                       |
| ------------ | ------------ | ----------------------------- |
| Chuck Norris | None         | Public API                    |
| Finance      | N/A          | Custom functions              |
| GitHub       | Bearer Token | `Bearer {token}`              |
| Jira         | Basic Auth   | `Basic {base64(email:token)}` |

### Tool Types

| Agent        | Tool Type        | How Tools Are Created             |
| ------------ | ---------------- | --------------------------------- |
| Hello        | None             | No tools                          |
| Chuck Norris | OpenAPI          | Auto-generated from spec          |
| Finance      | Custom Functions | Manually written Python functions |
| GitHub       | OpenAPI          | Auto-generated from spec          |
| Jira         | OpenAPI          | Auto-generated from spec          |

### Model Choices

| Agent        | Model            | Why?                    |
| ------------ | ---------------- | ----------------------- |
| Hello        | gemini-2.0-flash | Basic conversations     |
| Chuck Norris | gemini-2.0-flash | Simple tool calls       |
| Finance      | gemini-2.5-flash | Parallel tool execution |
| GitHub       | gemini-2.0-flash | Sequential workflow     |
| Jira         | gemini-2.5-flash | Parallel API calls      |

**Note:** Gemini 2.5 Flash has better parallel tool calling capabilities

---

## 💡 Key Learnings

### When to Use What

**Custom Python Functions:**

- ✅ Domain-specific calculations
- ✅ Complex business logic
- ✅ No external API needed
- ✅ Full control over implementation
- Example: Finance Assistant

**OpenAPI Tools (No Auth):**

- ✅ Public APIs
- ✅ Quick prototyping
- ✅ Learning tool generation
- Example: Chuck Norris Agent

**OpenAPI Tools (With Auth):**

- ✅ Private/authenticated APIs
- ✅ Real-world integrations
- ✅ Production use cases
- Examples: GitHub, Jira

### Parallel vs Sequential Execution

**Sequential (Default):**

- Tools called one after another
- Slower but simpler
- Good for dependent operations

**Parallel (Gemini 2.5 Flash):**

- Multiple tools called simultaneously
- Much faster for independent operations
- Requires explicit instructions to agent
- Example: "Get details for 5 issues" → 5 parallel calls

**How to Enable:**

1. Use `gemini-2.5-flash` model
2. Add instructions like: "When users ask about multiple items, call ALL tools in parallel"

---

## 🎯 Best Practices Learned

### OpenAPI Specs

1. Always validate `operationId` is unique
2. Use descriptive summaries and descriptions
3. Put `required` fields at schema level, not property level
4. Update server URLs with actual values at runtime
5. Test with real API documentation

### Authentication

1. Store credentials in `.env` files
2. Never hardcode tokens
3. Use appropriate auth type (Basic vs Bearer)
4. Handle auth errors gracefully

### Agent Instructions

1. Be specific about workflows
2. Include example interactions
3. Explain when to use which tool
4. For parallel execution, explicitly state it

### Tool Design

1. Return both structured data and human-readable messages
2. Include proper error handling
3. Validate inputs
4. Provide helpful error messages
