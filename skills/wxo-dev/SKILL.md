---
name: watsonx-orchestrate-development
description: |
  Expert guidance for building production-ready watsonx Orchestrate solutions using the ADK.
  Covers agents, tools, workflows, knowledge bases, MCP integration, security, testing, and deployment.
  Follows IBM best practices and official ADK patterns.
---

# watsonx Orchestrate Development

## Quick Start & Project Structure

### Essential Directories

```
project/
├── agents/              # Agent YAML configurations
├── tools/               # Python tools and flows
├── knowledge_bases/     # KB configurations and documents
├── models/              # LLM model configurations
├── toolkits/            # MCP toolkit definitions
├── connections/         # API connections and credentials
├── channels/            # Deployment channels (Slack, Teams, Web)
├── plugins/             # Guardrail and custom plugins
├── tests/               # Test cases and evaluation datasets
├── import-all.sh        # Comprehensive deployment script
├── requirements.txt     # Python dependencies (exclude ibm-watsonx-orchestrate)
├── .env.example         # Environment variable templates
└── README.md            # Architecture, setup, usage docs
```

### Environment Setup

**CRITICAL**: Choose ONE authentication method in `.env.example`:

**Option 1: watsonx Orchestrate (SaaS/Trial)**
```bash
WO_DEVELOPER_EDITION_SOURCE=orchestrate
WO_INSTANCE=https://your-instance.watson-orchestrate.ibm.com
WO_API_KEY=your-api-key-here
```

**Option 2: myIBM (On-premises/Purchased)**
```bash
WO_DEVELOPER_EDITION_SOURCE=myibm
WO_ENTITLEMENT_KEY=your-entitlement-key
GROQ_API_KEY=your-groq-api-key
WATSONX_APIKEY=your-watsonx-api-key
WATSONX_SPACE_ID=your-space-id
```

**Option 3: Custom Image Registry**
```bash
WO_DEVELOPER_EDITION_SOURCE=custom
REGISTRY_URL=your-registry-url
REGISTRY_USERNAME=your-username
REGISTRY_PASSWORD=your-password
```

**Important**: Never include actual credentials in `.env.example`. Do NOT use non-standard variables.

### Quick Commands

```bash
# Import agent
orchestrate agents import -f agents/my-agent.yaml

# Import Python tool
orchestrate tools import -k python -f tools/my-tool.py

# Import workflow
orchestrate tools import -k flow -f tools/my-workflow.py

# Import knowledge base
orchestrate knowledge-bases import -f knowledge_bases/my-kb.yaml

# Import MCP toolkit
orchestrate toolkits import -f toolkits/my-toolkit.yaml

# List all artifacts
orchestrate agents list
orchestrate tools list
orchestrate knowledge-bases list
orchestrate toolkits list

# Quick evaluation
orchestrate evaluations quick-eval -p tests/ -o results/ -t tools/
```

## Documentation & MCP Servers

### Using watsonx Orchestrate Documentation MCP Server

**CRITICAL**: When uncertain about watsonx Orchestrate features, syntax, or API references, ALWAYS use the `watsonx-orchestrate-adk-docs` MCP server to search official documentation before making assumptions.

#### When to Use the Documentation MCP Server

Use the MCP server to search for:
- **API References** - Tool decorators, flow builders, agent configurations
- **YAML Schemas** - Agent, toolkit, knowledge base, connection formats
- **Best Practices** - Recommended patterns, naming conventions, security guidelines
- **Feature Availability** - What's supported in Developer Edition vs SaaS vs On-premises
- **Troubleshooting** - Error messages, common issues, debugging techniques
- **CLI Commands** - Syntax, parameters, usage examples
- **Type Hints** - Correct parameter types for tools and flows
- **Environment Variables** - Official configuration options
- **Evaluation Metrics** - Available metrics and their meanings
- **Security Patterns** - Guardrails, connections, credential management

#### How to Search Documentation

The MCP server provides search capabilities for accurate, up-to-date information:

```bash
# Search for specific topics
search_docs("agent YAML schema")
search_docs("tool decorator syntax")
search_docs("MCP toolkit import")
search_docs("knowledge base document formats")
search_docs("evaluation config file")
```

**Search Strategy:**
1. **Start specific** - Search for exact feature names or error messages
2. **Broaden if needed** - Use general terms if specific search yields no results
3. **Cross-reference** - Verify information across multiple search results
4. **Check versions** - Ensure documentation matches your environment version

#### Examples of What to Look Up

**Before creating agents:**
```bash
search_docs("agent YAML structure")
search_docs("agent guidelines format")
search_docs("LLM model configuration")
```

**Before implementing tools:**
```bash
search_docs("@tool decorator parameters")
search_docs("tool type hints requirements")
search_docs("tool error handling patterns")
```

**Before building workflows:**
```bash
search_docs("agentic workflow structure")
search_docs("flow parameter mapping")
search_docs("workflow branching patterns")
```

**When encountering errors:**
```bash
search_docs("parameter parsing warning")
search_docs("connection authentication failed")
search_docs("knowledge base indexing status")
```

#### Other watsonx Orchestrate MCP Servers

The `watsonx-orchestrate-adk-docs` server is the primary documentation resource, but there may be other watsonx Orchestrate MCP servers available for different purposes:

- **API Integration Servers** - For connecting to external services
- **Data Processing Servers** - For specialized data transformations
- **Custom Toolkit Servers** - For domain-specific functionality

Check available MCP servers with:
```bash
orchestrate toolkits list
```

#### Important Notes

- **This skill complements official documentation** - Use the MCP server to access the most current information
- **Documentation is authoritative** - When this skill conflicts with official docs, trust the documentation
- **Stay updated** - watsonx Orchestrate evolves rapidly; always verify against latest docs
- **Search before assuming** - Don't guess at syntax or features; look them up
- **Document your findings** - Add discovered patterns to project README for team reference

**Best Practice**: Make searching documentation your first step when implementing new features or debugging issues. The MCP server provides faster, more accurate answers than trial-and-error.

---

---

## Agent Development

### Naming Conventions

**CRITICAL**: Agent names must follow strict rules for proper routing and identification.

**Required Format:**
- Use `snake_case` (underscores, not camelCase)
- No spaces allowed
- No special characters
- Keep names short and descriptive
- Use domain-specific language

**Examples:**

✅ **Good:**
- `customer_support_agent`
- `sales_outreach_agent`
- `ibm_historical_knowledge_agent`
- `product_catalog_agent`

❌ **Bad:**
- `customerSupportAgent` (camelCase)
- `customer support agent` (spaces)
- `agent-123` (special characters)
- `helper` (too generic)

### Default LLM Model

**IMPORTANT**: Use `groq/openai/gpt-oss-120b` as the default LLM model for all agents unless you have a specific reason to use a different model.

**Default Model:**
```yaml
llm: groq/openai/gpt-oss-120b
```

**Why This Model:**
- Optimized for watsonx Orchestrate platform
- Good balance of performance and cost
- Reliable for most agent tasks
- Well-tested with the platform

**Alternative Models:**
You can use other models by following the `provider/model-id` format:
- `openai/gpt-4` - For complex reasoning tasks
- `openai/gpt-5-2025-08-07` - Latest OpenAI model
- `anthropic/claude-3-opus` - For advanced capabilities

**Note:** When using external models (OpenAI, Anthropic, etc.), you must first:
1. Create a connection for the model provider
2. Import the model using `orchestrate models add`

### Agent YAML Structure

```yaml
spec_version: v1
kind: native
name: agent_name              # snake_case required
llm: groq/openai/gpt-oss-120b # Default LLM model
style: default                # Options: default, react, planner
hide_reasoning: false

description: |
  Clear description of agent purpose and capabilities

instructions: |
  General behavior, persona, and approach.
  Use for overall guidance and tone.

guidelines:
  - condition: "Specific trigger condition"
    action: "Specific action to take"
    tool: "tool_name"         # Only for tools, NOT collaborators

tools:
  - tool_name                 # Python tools
  - toolkit:tool_name         # MCP toolkit tools

collaborators:
  - other_agent_name          # For multi-agent collaboration

knowledge_base:
  - kb_name                   # Knowledge bases to use

restrictions: editable        # Options: editable, non_editable
```

### Guidelines vs Instructions

**Use Guidelines For:**
- Specific trigger conditions
- Rule-based responses
- Tool invocation rules
- Escalation triggers
- Conditional logic

**Use Instructions For:**
- General behavior and persona
- Tone and style guidance
- Context and background
- Overall approach
- Flexible decision-making

### Guidelines Structure

**CRITICAL**: Guidelines provide rule-based behavior control.

```yaml
guidelines:
  - condition: "When this situation occurs"
    action: "Then perform this action"
    tool: "tool_name"  # Optional: tool to invoke
```

**Required Fields:**
- `condition` (required): The trigger in natural language
- `action` (optional): The action to perform
- `tool` (optional): Tool name - MUST be from `tools` list, NOT collaborators

**Important**: You must provide at least one of `action` or `tool`.

**Collaborator Handoff Pattern:**
```yaml
- condition: "The customer mentions legal action"
  action: "Remain professional and hand off to the escalation_agent collaborator"
  # NOTE: Do NOT use tool field for collaborators
```

**Tool Invocation Pattern:**
```yaml
- condition: "The customer requests a refund under $500"
  action: "Process immediately and confirm 5-7 day timeline"
  tool: "process_refund"
```

**Ordering**: Place specific conditions before general ones.

### Multi-Agent Collaboration

- Design clear agent responsibilities and boundaries
- Use explicit handoff patterns in guidelines
- Document agent interaction flows
- Test multi-agent scenarios thoroughly

---

## Tools & Workflows

### Python Tools

**CRITICAL**: Import decorator correctly and use proper type hints.

```python
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from typing import Dict, Any

@tool
def my_tool(param: str) -> Dict[str, Any]:
    """
    Tool description.
    
    Args:
        param (str): Parameter description
        
    Returns:
        Dict[str, Any]: Result description
    """
    try:
        # Tool logic
        result = process_data(param)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

### Type Hints Requirements

**CRITICAL**: Type hints are required for proper schema generation.

**Standards:**
1. All parameters MUST have explicit type hints
2. Return types MUST be specified
3. Use specific types: `Dict[str, Any]` not `dict`
4. Type hints MUST match docstring descriptions
5. Import necessary typing constructs

**Common Mistakes:**

❌ **Wrong:**
```python
def my_tool(data: dict) -> Dict:  # Too generic
```

✅ **Correct:**
```python
def my_tool(data: Dict[str, Any]) -> Dict[str, Any]:  # Explicit
```

❌ **Wrong:**
```python
def my_tool(param: str):  # No return type
```

✅ **Correct:**
```python
def my_tool(param: str) -> Dict[str, Any]:  # Clear return type
```

### Agentic Workflows

**IMPORTANT**: Workflows are deterministic, predefined sequences - NOT agents with LLM reasoning.

**When to Use Workflows:**
- Process is deterministic and follows fixed sequence
- Steps are well-defined with clear inputs/outputs
- Need guaranteed execution order
- Performance critical (60% faster, 80% lower cost)
- No LLM reasoning needed between steps

**When to Use Agents:**
- Process requires dynamic decision-making
- Steps depend on LLM reasoning and context
- Flexibility more important than speed
- User interaction and conversation needed

**Workflow Structure:**

```python
from ibm_watsonx_orchestrate.flow_builder.flows import (
    Flow, flow, START, END, Branch
)
from pydantic import BaseModel, Field
from typing import Dict, Any

# 1. Define schemas
class WorkflowInput(BaseModel):
    customer_id: str = Field(description="Customer identifier")
    amount: float = Field(description="Transaction amount")

class WorkflowOutput(BaseModel):
    status: str = Field(description="Processing status")
    result: Dict[str, Any] = Field(description="Processing result")

# 2. Create workflow
@flow(
    name="my_workflow",
    description="Clear description",
    input_schema=WorkflowInput,
    output_schema=WorkflowOutput
)
def build_my_workflow(aflow: Flow) -> Flow:
    """
    Build the workflow graph.
    
    Args:
        aflow (Flow): The flow builder instance
        
    Returns:
        Flow: The configured flow
    """
    # 3. Define tool nodes (reference MCP tools)
    check_node = aflow.tool("toolkit-name:tool_name")
    
    # NOTE: watsonx Orchestrate uses automatic runtime data mapping
    # Tools automatically receive data when parameter names match expression references
    # No explicit map_input() calls needed - the platform handles this at runtime
    
    process_node = aflow.tool("toolkit-name:another_tool")
    
    # 4. Create branches
    decision_branch: Branch = aflow.branch(
        evaluator="check_node.output.status == 'approved'"
    )
    
    # 5. Build graph
    aflow.edge(START, check_node)
    aflow.edge(check_node, decision_branch)
    decision_branch.case(True, process_node)
    decision_branch.case(False, END)
    
    return aflow
```

**Automatic Data Mapping:**
- **IMPORTANT**: watsonx Orchestrate uses automatic runtime data mapping
- Tools receive data automatically when parameter names match workflow inputs or previous node outputs
- The platform resolves expressions like `flow.input.customer_id` and `check_node.output.status` at runtime
- No explicit mapping code is needed in the workflow definition
- Ensure tool parameter names match the data sources you want to reference

**Referencing Tools:**

**CRITICAL**: Tools must include toolkit prefix:

```python
# Correct - with toolkit prefix
check_credit = aflow.tool("loan-processing:check_credit_score")

# Wrong - without toolkit prefix (will fail)
check_credit = aflow.tool("check_credit_score")
```

**Importing Workflows:**

```bash
# Import workflow as flow-type tool
orchestrate tools import -k flow -f tools/my_workflow.py

# Verify import
orchestrate tools list | grep my_workflow
```

**Testing Workflows:**

Workflows can only be tested programmatically in Developer Edition. For other environments, test through agents.

```yaml
# Test via agent
tools:
  - my_workflow

guidelines:
  - condition: "User requests workflow execution"
    action: "Use my_workflow tool with required parameters"
    tool: "my_workflow"
```

---

## Knowledge Bases & MCP Integration

### Knowledge Base Format

**CRITICAL**: Documents must be external files, NOT inline content.

```yaml
spec_version: v1
kind: knowledge_base
name: kb_name
description: |
  Clear description of KB contents

documents:
  - path: document1.pdf      # Relative path to YAML file
  - path: docs/doc2.txt
  - path: ../shared/doc3.docx

vector_index:
  embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
  chunk_size: 400
  chunk_overlap: 50
  extraction_strategy: standard

conversational_search_tool:
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

**Supported Document Formats:**
- PDF (.pdf) - up to 25 MB
- Word (.docx) - up to 25 MB
- PowerPoint (.pptx) - up to 25 MB
- Excel (.xlsx) - up to 1 MB
- Text (.txt) - up to 5 MB
- CSV (.csv) - up to 5 MB
- HTML (.html) - up to 5 MB

**Limits:**
- Each file must have unique name
- Up to 100 files per KB
- Paths relative to YAML file

**Common Mistakes:**

❌ **Wrong - Inline content:**
```yaml
documents:
  - title: "Product 1"
    content: |
      Product information...
```

✅ **Correct - External files:**
```yaml
documents:
  - path: product_catalog.txt
  - path: faq_document.pdf
```

**Importing Knowledge Bases:**

```bash
# Import KB (uploads and indexes documents)
orchestrate knowledge-bases import -f knowledge_bases/my-kb.yaml

# Check status (wait for "ready")
orchestrate knowledge-bases get -n my_kb_name
```

**Using in Agents:**

```yaml
knowledge_base:
  - product_catalog_kb  # Must match KB name exactly
```

### MCP Toolkit Format

**CRITICAL**: Use official watsonx Orchestrate format for importing from files.

```yaml
spec_version: v1              # Required: Always v1
kind: mcp                     # Required: Must be "mcp"
name: toolkit-name            # Required: Toolkit identifier
description: "Description"    # Required: Clear purpose
command: python3 server.py    # Required: Single string command
env: []                       # Required: Environment variables
tools:
  - "*"                       # Use "*" for all tools
package_root: .               # Required: Path to MCP server
connections: []               # Optional: Connection app_ids
```

**Examples:**

**Python MCP Server:**
```yaml
spec_version: v1
kind: mcp
name: product-catalog
description: Product catalog MCP server
command: python3 product_catalog_server.py
env: []
tools:
  - "*"
package_root: .
```

**Node.js MCP Server:**
```yaml
spec_version: v1
kind: mcp
name: weather-service
description: Weather service
command: node dist/index.js
env: []
tools:
  - "*"
package_root: ./weather-server
```

**Import Methods:**

```bash
# Method 1: From YAML file (recommended)
orchestrate toolkits import -f toolkits/my-toolkit.yaml

# Method 2: Direct CLI
orchestrate toolkits add \
  --kind mcp \
  --name my-toolkit \
  --description "Toolkit description" \
  --package-root ./mcp_server \
  --command "python server.py" \
  --tools "*"
```

### Referencing MCP Tools in Agents

**CRITICAL**: Use full `toolkit-name:tool-name` format.

```yaml
tools:
  - product-catalog:search_products    # ✅ Correct
  - product-catalog:get_product_details
  - search_products                     # ❌ Wrong - missing prefix
```

**Verify tool names:**
```bash
orchestrate tools list | grep toolkit-name
```

---

## Security & Connections

### Guardrail Plugins

**CRITICAL**: Use correct decorator syntax with `kind` parameter.

**Pre-invoke Guardrails** (run BEFORE agent processes input):

```python
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.agent_builder.tools.types import (
    PythonToolKind,
    PluginContext,
    AgentPreInvokePayload,
    AgentPreInvokeResult
)

@tool(description="Filters inappropriate content", kind=PythonToolKind.AGENTPREINVOKE)
def content_safety_guardrail(plugin_context: PluginContext, 
                             agent_pre_invoke_payload: AgentPreInvokePayload) -> AgentPreInvokeResult:
    """Check for inappropriate content before processing."""
    result = AgentPreInvokeResult()
    
    # Check content
    if contains_inappropriate_content(user_message):
        # Block request
        result.continue_processing = False
        result.modified_payload = modified_payload
        return result
    
    # Allow through
    result.continue_processing = True
    result.modified_payload = agent_pre_invoke_payload
    return result
```

**Post-invoke Guardrails** (run AFTER agent generates response):

```python
from ibm_watsonx_orchestrate.agent_builder.tools.types import (
    PythonToolKind,
    AgentPostInvokePayload,
    AgentPostInvokeResult
)

@tool(description="Redacts PII from responses", kind=PythonToolKind.AGENTPOSTINVOKE)
def pii_filter_guardrail(plugin_context: PluginContext,
                        agent_post_invoke_payload: AgentPostInvokePayload) -> AgentPostInvokeResult:
    """Detect and redact PII in responses."""
    result = AgentPostInvokeResult()
    
    # Redact PII patterns
    response_text = redact_pii(response_text)
    
    result.continue_processing = True
    result.modified_payload = modified_payload
    return result
```

**Attaching to Agents:**

```yaml
plugins:
  agent_pre_invoke:
    - plugin_name: content_safety_guardrail
  agent_post_invoke:
    - plugin_name: pii_filter_guardrail
```

**Important**: Plugins must be imported before referencing in agent YAML.

### Creating Connections

**For External Model APIs** (3-step process):

```bash
# Step 1: Add connection
orchestrate connections add --app-id openai --env draft
orchestrate connections add --app-id openai --env live

# Step 2: Configure (use key_value for API keys)
orchestrate connections configure --app-id openai --env draft --type team --kind key_value
orchestrate connections configure --app-id openai --env live --type team --kind key_value

# Step 3: Set credentials
orchestrate connections set-credentials --app-id openai --env draft --entries "api_key=$OPENAI_API_KEY"
orchestrate connections set-credentials --app-id openai --env live --entries "api_key=$OPENAI_API_KEY"
```

**Parameters:**
- `--type team` - Shared credentials (use `member` for per-user)
- `--kind key_value` - Flexible key-value pairs for authentication
- Key name "api_key" for consistency

**Importing External Models:**

```bash
# Add model (no --env parameter)
orchestrate models add --name openai/gpt-4 --app-id openai

# Verify
orchestrate models list
```

### Security Checklist

- ✅ Never hardcode credentials
- ✅ Use connections for all external APIs
- ✅ Sanitize all inputs
- ✅ Implement guardrails for sensitive operations
- ✅ Use least privilege permissions
- ✅ Audit logging for security events
- ✅ Regular security testing

---

## Testing & Evaluation

### Testing Python Tools

**CRITICAL**: Test files must NOT import decorated functions.

The `@tool` decorator changes return behavior. Create standalone test versions:

```python
"""
Test cases for my_tool.

Note: Copy tool logic WITHOUT @tool decorator for testing.
"""

from typing import Dict

def my_tool(param: str) -> Dict:
    """
    Test version without @tool decorator.
    Copy exact business logic from tools/my_tool.py
    """
    try:
        result = process_data(param)
        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

def test_successful_case():
    result = my_tool("test")
    assert result['status'] == 'success'
    print("✓ Test passed")

if __name__ == "__main__":
    test_successful_case()
```

**Why**: Decorated functions return data in framework-specific format incompatible with direct testing.

### Evaluation Configuration

**CRITICAL**: Metrics are auto-computed, NOT configurable.

**For Developer Edition (Local):**
```yaml
test_paths:
  - evaluation/datasets/

auth_config:
  url: http://localhost:4321
  tenant_name: local

output_dir: evaluation/results/
enable_verbose_logging: true
n_runs: 1
```

**For SaaS:**
```yaml
test_paths:
  - evaluation/datasets/

auth_config:
  url: https://api.<region>.watson-orchestrate.ibm.com/instances/<instance-id>
  tenant_name: saas

output_dir: evaluation/results/
enable_verbose_logging: true
wxo_lite_version: 1.12.0
n_runs: 1
```

**Available Metrics** (auto-computed):
- Tool Calls, Successful Tool Calls
- Schema Mismatch, Hallucination
- Response/Retrieval Confidence
- Faithfulness, Answer Relevancy
- Tool Call Precision/Recall
- Agent Routing Accuracy
- Text Match, Journey Success

**Common Mistakes:**

❌ **Wrong - Trying to configure metrics:**
```yaml
metrics:
  - response_confidence
```

✅ **Correct - Metrics auto-computed:**
```yaml
# No metrics configuration needed
```

### Quick Evaluation

```bash
# Quick evaluation (reference-less)
orchestrate evaluations quick-eval -p evaluation/datasets/ -o results/ -t tools/

# With config file
orchestrate evaluations quick-eval -c evaluation/config.yaml
```

### Evaluation Datasets

**Format**: JSON files (not JSONL) with structured ground truth.

Each test case is a separate JSON file:
```json
{
    "agent": "my_agent",
    "goals": {
        "tool_call-1": ["summarize"]
    },
    "goal_details": [
        {
            "type": "tool_call",
            "name": "tool_call-1",
            "tool_name": "my_tool",
            "args": {"param": "value"}
        },
        {
            "name": "summarize",
            "type": "text",
            "response": "Expected response",
            "keywords": ["key", "terms"]
        }
    ],
    "story": "User story context",
    "starting_sentence": "User's initial query"
}
```

### Red-Teaming

```bash
# List attack types
orchestrate evaluations red-teaming list

# Plan attacks
orchestrate evaluations red-teaming plan \
  -a "instruction_override,crescendo_attack,jailbreaking" \
  -d evaluation/test-cases.jsonl \
  -t agent_name \
  -o evaluation/red-team-attacks/ \
  -n 3

# Run attacks
orchestrate evaluations red-teaming run \
  -a evaluation/red-team-attacks/ \
  -o evaluation/red-team-results/
```

---

## Deployment & Channels

### Supported Channels

- **webchat** (auto-available)
- **twilio_whatsapp**, **twilio_sms**
- **byo_slack**, **teams**
- **genesys_bot_connector**

### Channel Configuration

**Slack Channel:**
```yaml
name: customer-support-slack
type: slack
agent: customer-support-agent
settings:
  workspace_id: ${SLACK_WORKSPACE_ID}
  bot_token: ${SLACK_BOT_TOKEN}
```

**Web Chat Channel:**
```yaml
name: website-chat
type: web
agent: product-assistant
settings:
  theme: light
  welcome_message: "How can I help you today?"
```

### Deployment Process

**CRITICAL**: Import order matters! Dependencies must be imported before the agents that reference them.

**Correct Import Order:**

1. **Connections** (if using external APIs or models)
2. **Models** (if using external LLMs)
3. **Guardrail Plugins** (if agents use pre/post-invoke plugins)
4. **MCP Toolkits** (if using MCP servers)
5. **Python Tools** (individual tools)
6. **Workflows** (agentic workflows/flows)
7. **Knowledge Bases** (document collections)
8. **Collaborator Agents** (agents that will be called by other agents)
9. **Orchestrator Agents** (agents that reference collaborators)

**Why Order Matters:**
- Agents cannot be imported if they reference tools, knowledge bases, collaborators, or guardrails that don't exist yet
- Guardrail plugins must exist before agents that reference them in their `plugins` section
- Tools in workflows must exist before the workflow is imported
- Collaborator agents must exist before orchestrator agents that call them
- Connections must exist before models that use them

**Example Import Script:**
```bash
#!/bin/bash
set -e

echo "🚀 Importing watsonx Orchestrate artifacts in correct order..."

# 1. Connections (for external APIs/models)
echo "🔗 Importing connections..."
for file in connections/*.yaml; do
    [ -f "$file" ] && orchestrate connections import -f "$file"
done

# 2. Models (external LLMs)
echo "🤖 Importing models..."
# orchestrate models add --name openai/gpt-4 --app-id openai

# 3. Guardrail Plugins (MUST be before agents that use them)
echo "🛡️ Importing guardrail plugins..."
for file in plugins/*.py; do
    [ -f "$file" ] && orchestrate tools import -k python -f "$file"
done

# 4. MCP Toolkits
echo "🧰 Importing MCP toolkits..."
for file in toolkits/*.yaml; do
    [ -f "$file" ] && orchestrate toolkits import -f "$file"
done

# 5. Python Tools
echo "🔧 Importing Python tools..."
for file in tools/*.py; do
    [ -f "$file" ] && [[ ! "$file" =~ _workflow\.py$ ]] && \
        orchestrate tools import -k python -f "$file"
done

# 6. Workflows (agentic workflows)
echo "🔄 Importing workflows..."
for file in tools/*_workflow.py; do
    [ -f "$file" ] && orchestrate tools import -k flow -f "$file"
done

# 7. Knowledge Bases
echo "📚 Importing knowledge bases..."
for file in knowledge_bases/*.yaml; do
    [ -f "$file" ] && orchestrate knowledge-bases import -f "$file"
done

# 8. Collaborator Agents (imported before orchestrators)
echo "👥 Importing collaborator agents..."
# Import specific collaborator agents first
[ -f "agents/escalation-agent.yaml" ] && orchestrate agents import -f "agents/escalation-agent.yaml"
[ -f "agents/specialist-agent.yaml" ] && orchestrate agents import -f "agents/specialist-agent.yaml"

# 9. Orchestrator Agents (reference collaborators)
echo "🎯 Importing orchestrator agents..."
for file in agents/*.yaml; do
    # Skip already imported collaborators
    if [ -f "$file" ] && [[ ! "$file" =~ (escalation|specialist)-agent\.yaml$ ]]; then
        orchestrate agents import -f "$file"
    fi
done

echo "✅ Import complete!"
echo ""
echo "Verify with:"
echo "  orchestrate agents list"
echo "  orchestrate tools list"
echo "  orchestrate knowledge-bases list"
```

**Quick Verification:**
```bash
# Verify all artifacts imported successfully
orchestrate agents list
orchestrate tools list
orchestrate toolkits list
orchestrate knowledge-bases list
orchestrate connections list
```

**Deployment (SaaS/On-Premises only):**
```bash
# Deploy agent (not available in Developer Edition)
orchestrate agents deploy --name my-agent

# Deploy channels
orchestrate channels deploy channel-name
```

### Channel Management

```bash
# List channels for agent
orchestrate channels list-channels --agent-name my-agent --env draft

# Import channel from file
orchestrate channels import --agent-name my-agent --env draft --file channels/my-channel.yaml

# Export channel
orchestrate channels export --agent-name my-agent --env draft --type webchat --name my-channel -o channel.yaml

# Delete channel
orchestrate channels delete --agent-name my-agent --env draft --type webchat --name my-channel
```

### Environment-Specific Configs

- **Development** - Test credentials, verbose logging
- **Staging** - Mirror production, staging APIs
- **Production** - Production credentials, optimized settings

---

## Troubleshooting & Optimization

### Common Errors

**Error: Tool not found**
```bash
# Verify tool is imported
orchestrate tools list

# Check tool name matches decorator
```

**Error: "required property" in workflow**
```python
# Ensure tool parameter names match the data sources being referenced
# The platform automatically maps data at runtime based on parameter names
# Example: If tool expects "customer_id", workflow input should have "customer_id"
# No explicit mapping code needed - automatic runtime resolution
```

**Error: Connection failed**
```bash
# Verify connection exists
orchestrate connections list

# Check credentials are set
orchestrate connections get -a connection-name
```

**Error: Agent timeout**
- Optimize tool execution time
- Reduce complexity of operations
- Implement caching
- Use async operations

**Error: Token limit exceeded**
- Reduce context size
- Optimize prompts
- Use conversation summarization
- Choose appropriate model size

**Error: Knowledge base not found**
```bash
# Check KB status (should be "ready")
orchestrate knowledge-bases get -n kb_name

# Verify KB name matches exactly in agent YAML
```

### Performance Optimization

**Token Usage:**
- Use concise, clear prompts
- Avoid redundant context
- Implement conversation summarization
- Choose appropriate model sizes

**Caching:**
- Cache frequently accessed data
- Implement response caching for common queries
- Use knowledge bases for static information
- Cache API responses when appropriate

**Workflows:**
- Use workflows for deterministic processes (60% faster)
- Implement parallel execution where possible
- Optimize tool chaining
- Monitor execution times

**Model Selection:**
- Simple tasks → smaller, faster models
- Complex reasoning → larger, capable models
- Cost-sensitive → balance performance vs. cost
- Latency-sensitive → prioritize faster models

### Debugging Workflow

1. **Test tools independently** (without decorator)
2. **Verify imports**: `orchestrate tools list`
3. **Check logs** for errors and warnings
4. **Use quick-eval** for validation
5. **Monitor metrics** (tokens, latency, success rates)

### Log Analysis

- Check agent execution logs for errors
- Review tool invocation logs
- Analyze token usage patterns
- Monitor response times
- Track success/failure rates

---

## Quick Reference

### Essential Commands

```bash
# Agents
orchestrate agents import -f agents/my-agent.yaml
orchestrate agents list
orchestrate agents remove --name my-agent

# Tools
orchestrate tools import -k python -f tools/my-tool.py
orchestrate tools import -k flow -f tools/my-workflow.py
orchestrate tools list
orchestrate tools remove -n my-tool

# Toolkits
orchestrate toolkits import -f toolkits/my-toolkit.yaml
orchestrate toolkits list
orchestrate toolkits remove -n my-toolkit

# Knowledge Bases
orchestrate knowledge-bases import -f knowledge_bases/my-kb.yaml
orchestrate knowledge-bases list
orchestrate knowledge-bases get -n my-kb

# Connections
orchestrate connections add --app-id my-connection --env draft
orchestrate connections configure --app-id my-connection --env draft --type team --kind key_value
orchestrate connections set-credentials --app-id my-connection --env draft --entries "api_key=$API_KEY"
orchestrate connections list

# Models
orchestrate models add --name provider/model-name --app-id connection-name
orchestrate models list

# Evaluation
orchestrate evaluations quick-eval -p tests/ -o results/ -t tools/
orchestrate evaluations quick-eval -c evaluation/config.yaml

# Channels
orchestrate channels list-channels --agent-name my-agent --env draft
orchestrate channels import --agent-name my-agent --env draft --file channels/my-channel.yaml
```

### Best Practices Summary

1. **Always use CLI** for importing agents and tools
2. **Test locally first** before deploying to production
3. **Use connections** for all external API integrations
4. **Implement guardrails** for safety and compliance
5. **Document everything** - code, configurations, workflows
6. **Version control** all artifacts and configurations
7. **Monitor performance** - tokens, latency, success rates
8. **Security first** - never commit credentials, sanitize inputs
9. **Evaluate regularly** - maintain test cases, run evaluations
10. **Use workflows** for deterministic processes (60% faster, 80% lower cost)

### Decision Matrices

**Tool vs Workflow:**
| Criteria | Use Tool | Use Workflow |
|----------|----------|--------------|
| Process Type | Single operation | Multi-step sequence |
| LLM Reasoning | May need reasoning | No reasoning needed |
| Execution Order | N/A | Fixed, guaranteed |
| Performance | Standard | 60% faster |
| Cost | Standard | 80% lower |

**Guidelines vs Instructions:**
| Criteria | Use Guidelines | Use Instructions |
|----------|----------------|------------------|
| Purpose | Specific rules | General behavior |
| Trigger | Condition-based | Always active |
| Action | Explicit | Flexible |
| Tool Invocation | Yes | No |
| Predictability | High | Variable |

---

## Additional Resources

- **examples.md** - Complete working examples and implementations
- **references/project-structure.md** - Detailed project organization
- **references/yaml-schemas.md** - Complete YAML schema documentation
- **references/cli-commands.md** - Comprehensive CLI reference
- **references/troubleshooting.md** - Exhaustive error catalog
- **scripts/** - Ready-to-use automation scripts
- **templates/** - Copy-paste starting points for common artifacts