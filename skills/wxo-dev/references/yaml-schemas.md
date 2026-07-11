# YAML Schema Reference

Complete YAML schema documentation for watsonx Orchestrate artifacts.

## Agent YAML Schema

### Complete Agent Structure

```yaml
spec_version: v1                 # Required: Always "v1"
kind: native                     # Required: "native" for standard agents
name: agent_name                 # Required: snake_case, no spaces
llm: groq/openai/gpt-oss-120b   # Required: LLM model identifier
style: default                   # Optional: default, react, planner
hide_reasoning: false            # Optional: Show/hide reasoning steps

description: |                   # Required: Multi-line description
  Clear description of agent purpose and capabilities.
  What the agent does and when to use it.

instructions: |                  # Required: General behavior guidance
  Detailed instructions for agent behavior.
  Persona, tone, approach, and general guidelines.
  Use for overall guidance, not specific rules.

guidelines:                      # Optional: Rule-based behavior
  - condition: "Trigger condition in natural language"
    action: "Action to take when condition is met"
    tool: "tool_name"           # Optional: Tool to invoke

tools:                          # Optional: List of tools
  - tool_name                   # Python tools
  - toolkit:tool_name           # MCP toolkit tools

collaborators:                  # Optional: Other agents
  - other_agent_name

knowledge_base:                 # Optional: Knowledge bases
  - kb_name

plugins:                        # Optional: Guardrail plugins
  agent_pre_invoke:
    - plugin_name: pre_invoke_plugin
  agent_post_invoke:
    - plugin_name: post_invoke_plugin

restrictions: editable          # Optional: editable, non_editable
hidden: false                   # Optional: Hide from UI
```

### Field Descriptions

#### spec_version
- **Type:** String
- **Required:** Yes
- **Value:** Always "v1"
- **Description:** Schema version identifier

#### kind
- **Type:** String
- **Required:** Yes
- **Values:** "native"
- **Description:** Agent type (currently only "native" supported)

#### name
- **Type:** String
- **Required:** Yes
- **Format:** snake_case, no spaces, no special characters
- **Description:** Unique agent identifier
- **Examples:** `customer_support_agent`, `sales_outreach_agent`

#### llm
- **Type:** String
- **Required:** Yes
- **Format:** `provider/model-id`
- **Default:** `groq/openai/gpt-oss-120b`
- **Description:** LLM model to use
- **Examples:**
  - `groq/openai/gpt-oss-120b`
  - `openai/gpt-4`
  - `anthropic/claude-3-opus`

#### style
- **Type:** String
- **Required:** No
- **Default:** "default"
- **Values:** "default", "react", "planner"
- **Description:** Agent reasoning style

#### hide_reasoning
- **Type:** Boolean
- **Required:** No
- **Default:** false
- **Description:** Whether to hide reasoning steps in UI

#### description
- **Type:** String (multi-line)
- **Required:** Yes
- **Description:** Clear description of agent purpose and capabilities

#### instructions
- **Type:** String (multi-line)
- **Required:** Yes
- **Description:** General behavior guidance, persona, and approach

#### guidelines
- **Type:** Array of objects
- **Required:** No
- **Description:** Rule-based behavior control
- **Structure:**
  ```yaml
  - condition: "String"  # Required
    action: "String"     # Optional
    tool: "String"       # Optional (must be from tools list)
  ```

#### tools
- **Type:** Array of strings
- **Required:** No
- **Description:** List of tools available to agent
- **Format:**
  - Python tools: `tool_name`
  - MCP tools: `toolkit:tool_name`

#### collaborators
- **Type:** Array of strings
- **Required:** No
- **Description:** List of other agents for collaboration

#### knowledge_base
- **Type:** Array of strings
- **Required:** No
- **Description:** List of knowledge bases to use

#### plugins
- **Type:** Object
- **Required:** No
- **Description:** Guardrail plugins
- **Structure:**
  ```yaml
  agent_pre_invoke:
    - plugin_name: plugin_name
  agent_post_invoke:
    - plugin_name: plugin_name
  ```

#### restrictions
- **Type:** String
- **Required:** No
- **Default:** "editable"
- **Values:** "editable", "non_editable"
- **Description:** Whether agent can be edited in UI

#### hidden
- **Type:** Boolean
- **Required:** No
- **Default:** false
- **Description:** Whether to hide agent from UI

---

## Knowledge Base YAML Schema

### Complete KB Structure

```yaml
spec_version: v1                # Required: Always "v1"
kind: knowledge_base            # Required: Always "knowledge_base"
name: kb_name                   # Required: Unique identifier
description: |                  # Required: KB description
  Clear description of KB contents and purpose.

documents:                      # Required: List of documents
  - path: document1.pdf         # Relative path to YAML file
  - path: docs/document2.txt
  - path: ../shared/doc3.docx

vector_index:                   # Optional: Vector index settings
  embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
  chunk_size: 400
  chunk_overlap: 50
  extraction_strategy: standard

conversational_search_tool:     # Optional: Search tool settings
  generation:
    prompt_instruction: "Instructions for answering questions"
    max_docs_passed_to_llm: 10
    generated_response_length: Moderate
    idk_message: "Message when answer not found"
  confidence_thresholds:
    retrieval_confidence_threshold: Low
    response_confidence_threshold: Low
  query_rewrite:
    enabled: true
  citations:
    citations_shown: -1
```

### Field Descriptions

#### documents
- **Type:** Array of objects
- **Required:** Yes
- **Description:** List of document files
- **Structure:**
  ```yaml
  - path: relative/path/to/document.pdf
  ```
- **Supported Formats:**
  - PDF (.pdf) - up to 25 MB
  - Word (.docx) - up to 25 MB
  - PowerPoint (.pptx) - up to 25 MB
  - Excel (.xlsx) - up to 1 MB
  - Text (.txt) - up to 5 MB
  - CSV (.csv) - up to 5 MB
  - HTML (.html) - up to 5 MB

#### vector_index.embeddings_model_name
- **Type:** String
- **Default:** `ibm/slate-125m-english-rtrvr-v2`
- **Description:** Embedding model for vector indexing

#### vector_index.chunk_size
- **Type:** Integer
- **Default:** 400
- **Description:** Size of text chunks for indexing

#### vector_index.chunk_overlap
- **Type:** Integer
- **Default:** 50
- **Description:** Overlap between chunks

#### vector_index.extraction_strategy
- **Type:** String
- **Default:** "standard"
- **Description:** Document extraction strategy

#### conversational_search_tool.generation.generated_response_length
- **Type:** String
- **Values:** "Short", "Moderate", "Long"
- **Default:** "Moderate"
- **Description:** Length of generated responses

#### conversational_search_tool.confidence_thresholds
- **Values:** "Low", "Medium", "High"
- **Description:** Confidence thresholds for retrieval and response

---

## MCP Toolkit YAML Schema

### Complete Toolkit Structure

```yaml
spec_version: v1                # Required: Always "v1"
kind: mcp                       # Required: Always "mcp"
name: toolkit-name              # Required: Unique identifier
description: "Toolkit description"  # Required: Clear purpose
command: python3 server.py      # Required: Single string command
env: []                         # Required: Environment variables
tools:                          # Required: Tools to import
  - "*"                         # "*" for all, or list specific tools
package_root: .                 # Required: Path to MCP server
connections: []                 # Optional: Connection app_ids
```

### Field Descriptions

#### command
- **Type:** String
- **Required:** Yes
- **Format:** Single command string
- **Examples:**
  - `python3 server.py`
  - `node dist/index.js`
  - `./run_server.sh`

#### env
- **Type:** Array of objects
- **Required:** Yes (can be empty)
- **Description:** Environment variables for server
- **Structure:**
  ```yaml
  env:
    - name: VAR_NAME
      value: var_value
  ```

#### tools
- **Type:** Array of strings
- **Required:** Yes
- **Description:** Tools to import from server
- **Values:**
  - `"*"` - Import all tools
  - `["tool1", "tool2"]` - Import specific tools

#### package_root
- **Type:** String
- **Required:** Yes
- **Description:** Path to MCP server package (relative to YAML)
- **Examples:** `.`, `./server`, `../shared/mcp-server`

#### connections
- **Type:** Array of strings
- **Required:** No
- **Description:** Connection app_ids to bind to toolkit

---

## Connection YAML Schema

### Complete Connection Structure

```yaml
name: connection-name           # Required: Unique identifier
type: http                      # Required: Connection type
auth:                          # Required: Authentication config
  type: bearer_token           # Auth type
  token: ${API_TOKEN}          # From environment variable
```

### Connection Types

#### HTTP Connection
```yaml
name: api-connection
type: http
auth:
  type: bearer_token
  token: ${API_TOKEN}
```

#### OAuth Connection
```yaml
name: oauth-connection
type: oauth2
auth:
  type: oauth2
  client_id: ${CLIENT_ID}
  client_secret: ${CLIENT_SECRET}
  token_url: https://auth.example.com/token
```

#### API Key Connection
```yaml
name: api-key-connection
type: http
auth:
  type: api_key
  api_key: ${API_KEY}
  header_name: X-API-Key
```

---

## Channel YAML Schema

### Slack Channel

```yaml
name: channel-name              # Required: Unique identifier
type: slack                     # Required: Channel type
agent: agent-name               # Required: Agent to deploy
settings:                       # Required: Channel-specific settings
  workspace_id: ${SLACK_WORKSPACE_ID}
  bot_token: ${SLACK_BOT_TOKEN}
```

### Web Chat Channel

```yaml
name: channel-name
type: web
agent: agent-name
settings:
  theme: light                  # light or dark
  welcome_message: "Welcome message"
  primary_color: "#0066cc"
```

### Teams Channel

```yaml
name: channel-name
type: teams
agent: agent-name
settings:
  app_id: ${TEAMS_APP_ID}
  app_password: ${TEAMS_APP_PASSWORD}
```

---

## Workflow Schema (Python)

### Complete Workflow Structure

```python
from ibm_watsonx_orchestrate.flow_builder.flows import Flow, flow, START, END, Branch
from pydantic import BaseModel, Field
from typing import Dict, Any

class WorkflowInput(BaseModel):
    """Input schema"""
    param: str = Field(description="Parameter description")

class WorkflowOutput(BaseModel):
    """Output schema"""
    result: str = Field(description="Result description")

@flow(
    name="workflow_name",
    description="Workflow description",
    input_schema=WorkflowInput,
    output_schema=WorkflowOutput
)
def build_workflow(aflow: Flow) -> Flow:
    """
    Build workflow graph.
    
    NOTE: watsonx Orchestrate uses automatic runtime data mapping.
    Tools receive data automatically when parameter names match workflow
    inputs or previous node outputs. No explicit mapping code needed.
    """
    # Define nodes - tools automatically receive matching parameters
    node = aflow.tool("toolkit:tool_name")
    
    # Build graph
    aflow.edge(START, node)
    aflow.edge(node, END)
    
    return aflow
```

### @flow Decorator Parameters

- **name** (required): Workflow identifier
- **description** (required): Clear description
- **input_schema** (required): Pydantic model for input
- **output_schema** (required): Pydantic model for output

### Node Types

#### Tool Node
```python
# Tools automatically receive data at runtime based on parameter names
node = aflow.tool("toolkit:tool_name")
# No explicit mapping needed - automatic resolution of:
# - flow.input.param_name
# - previous_node.output.field_name
```

#### Branch Node
```python
branch: Branch = aflow.branch(evaluator="condition")
branch.case(True, true_node)
branch.case(False, false_node)
```

#### Foreach Node
```python
foreach = aflow.foreach(items="input.items", body=process_node)
```

---

## Validation Rules

### Agent Validation
- Name must be snake_case
- LLM must be valid model identifier
- Tools must exist before agent import
- Collaborators must exist before agent import
- Knowledge bases must exist before agent import

### Knowledge Base Validation
- Documents must exist at specified paths
- Document files must have unique names
- Maximum 100 documents per KB
- File sizes must be within limits

### MCP Toolkit Validation
- Command must be executable
- Package root must exist
- Tools must be valid MCP tools

### Workflow Validation
- Input/output schemas must be Pydantic models
- Tool references must include toolkit prefix
- All nodes must be connected to graph

---

## LangGraph Agent YAML Schema

### Complete LangGraph Agent Structure

```yaml
spec_version: v1                # Required: Always "v1"
kind: agent                     # Required: Always "agent" for LangGraph
name: agent_name                # Required: snake_case, no spaces
title: Agent Title              # Required: Human-readable title
description: |                  # Required: Multi-line description
  Clear description of agent purpose and capabilities.
  What the agent does and when to use it.

framework: langgraph            # Required: Always "langgraph"

deployment:                     # Required: Deployment configuration
  code_bundle:
    entrypoint: module:function # Required: Factory function path

checkpointer:                   # Optional: State persistence
  type: memory                  # memory, sqlite, postgres
  connection_string_key: conn   # Required for postgres
```

### Field Descriptions

#### spec_version
- **Type:** String
- **Required:** Yes
- **Value:** Always "v1"
- **Description:** Schema version identifier

#### kind
- **Type:** String
- **Required:** Yes
- **Value:** Always "agent" for LangGraph agents
- **Description:** Agent type identifier

#### name
- **Type:** String
- **Required:** Yes
- **Format:** snake_case, no spaces, no special characters
- **Description:** Unique agent identifier
- **Examples:** `research_agent`, `customer_support_agent`

#### title
- **Type:** String
- **Required:** Yes
- **Description:** Human-readable agent name for UI display
- **Examples:** "Research Agent", "Customer Support Agent"

#### description
- **Type:** String (multi-line)
- **Required:** Yes
- **Description:** Clear description of agent purpose and capabilities

#### framework
- **Type:** String
- **Required:** Yes
- **Value:** Always "langgraph"
- **Description:** Framework identifier

#### deployment.code_bundle.entrypoint
- **Type:** String
- **Required:** Yes
- **Format:** `module:function` or `module.submodule:function`
- **Description:** Path to factory function that creates StateGraph
- **Examples:**
  - `agent:create_agent`
  - `src.agent:build_graph`
  - `core.graph:create_research_agent`

#### checkpointer.type
- **Type:** String
- **Required:** No
- **Values:** "memory", "sqlite", "postgres"
- **Default:** "memory"
- **Description:** State persistence mechanism
- **Details:**
  - **memory**: In-memory only, no persistence across restarts
  - **sqlite**: File-based persistence, single-instance only
  - **postgres**: Database persistence, supports multi-instance

#### checkpointer.connection_string_key
- **Type:** String
- **Required:** Yes (when type is "postgres")
- **Description:** Key name in connection for PostgreSQL connection string
- **Example:** `postgres_connection`

### LangGraph Agent Package Structure

```
agent-name/
├── agent.yaml              # Required: Agent configuration
├── agent.py                # Required: Factory function
├── requirements.txt        # Required: Python dependencies
└── core/                   # Optional: Additional modules
    ├── __init__.py
    ├── state.py
    └── nodes.py
```

### Factory Function Requirements

```python
from langgraph.graph import StateGraph
from typing import TypedDict

class AgentState(TypedDict):
    """State definition"""
    field1: str
    field2: int

def create_agent() -> StateGraph:
    """
    Factory function that creates the agent.
    
    CRITICAL: Must return UNCOMPILED StateGraph.
    The platform compiles the graph at runtime.
    
    Returns:
        StateGraph: Uncompiled StateGraph instance
    """
    graph = StateGraph(AgentState)
    
    # Add nodes
    graph.add_node("node1", node1_function)
    graph.add_node("node2", node2_function)
    
    # Define flow
    graph.set_entry_point("node1")
    graph.add_edge("node1", "node2")
    graph.add_edge("node2", END)
    
    return graph  # Return uncompiled - DO NOT call .compile()
```

### Checkpointer Examples

#### Memory Checkpointer (Default)
```yaml
checkpointer:
  type: memory
```

#### SQLite Checkpointer
```yaml
checkpointer:
  type: sqlite
```

#### PostgreSQL Checkpointer
```yaml
checkpointer:
  type: postgres
  connection_string_key: postgres_connection
```

**PostgreSQL Connection Setup:**
```bash
# Create connection
orchestrate connections add --app-id postgres --env draft
orchestrate connections configure --app-id postgres --env draft --type team --kind key_value

# Set connection string
orchestrate connections set-credentials --app-id postgres --env draft \
  --entries "postgres_connection=postgresql://user:pass@host:5432/dbname"
```

### Complete Example

```yaml
spec_version: v1
kind: agent
name: customer_support_agent
title: Customer Support Agent
description: |
  Handles customer inquiries with context persistence.
  Provides personalized support based on conversation history.

framework: langgraph

deployment:
  code_bundle:
    entrypoint: agent:create_agent

checkpointer:
  type: postgres
  connection_string_key: postgres_connection
```

### Validation Rules

#### LangGraph Agent Validation
- Name must be snake_case
- Title must be provided
- Framework must be "langgraph"
- Entrypoint must point to valid factory function
- Factory function must return uncompiled StateGraph
- LangGraph version must be >= 0.6.0
- Checkpointer type must be valid
- PostgreSQL connection must exist if using postgres checkpointer

#### Platform Availability
- **Supported:** Commercial AWS regions, IBM Cloud regions
- **Not Supported:** On-premises deployments, GovCloud regions

#### Import Requirements
- Package must contain agent.yaml
- Package must contain Python file with factory function
- requirements.txt must include langgraph>=0.6.0
- All dependencies must be installable from PyPI

### Common Mistakes

❌ **Wrong - Compiled StateGraph:**
```python
def create_agent() -> StateGraph:
    graph = StateGraph(State)
    # ... add nodes ...
    return graph.compile()  # WRONG - Do not compile
```

✅ **Correct - Uncompiled StateGraph:**
```python
def create_agent() -> StateGraph:
    graph = StateGraph(State)
    # ... add nodes ...
    return graph  # CORRECT - Return uncompiled
```

❌ **Wrong - Missing title:**
```yaml
spec_version: v1
kind: agent
name: my_agent
framework: langgraph
```

✅ **Correct - With title:**
```yaml
spec_version: v1
kind: agent
name: my_agent
title: My Agent
framework: langgraph
```

❌ **Wrong - Invalid entrypoint format:**
```yaml
deployment:
  code_bundle:
    entrypoint: agent.create_agent  # Wrong separator
```

✅ **Correct - Colon separator:**
```yaml
deployment:
  code_bundle:
    entrypoint: agent:create_agent  # Correct
```

### Import Command

```bash
# Import LangGraph agent
orchestrate agents import -k langgraph -f agent-directory/

# Verify import
orchestrate agents list | grep agent_name
```

### Using LangGraph Agents as Collaborators

LangGraph agents can be used as collaborators in native agents:

```yaml
# Native agent YAML
spec_version: v1
kind: native
name: orchestrator_agent
llm: groq/openai/gpt-oss-120b

collaborators:
  - customer_support_agent  # LangGraph agent

guidelines:
  - condition: "User needs customer support"
    action: "Hand off to customer_support_agent collaborator"
```

**Import Order:**
```bash
# 1. Import LangGraph agent first
orchestrate agents import -k langgraph -f customer-support-agent/

# 2. Import native agent that references it
orchestrate agents import -f orchestrator-agent.yaml
```
- Graph must have START and END nodes