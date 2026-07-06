# watsonx Orchestrate Development Skill - Design Document

## Executive Summary

This document outlines the structure and organization for converting the comprehensive watsonx Orchestrate development rule (2194 lines, 10 major areas) into a condensed, high-signal skill specification following the Agent Skills format.

**Goal:** Create a skill that helps coding agents build watsonx Orchestrate solutions following IBM best practices, with progressive disclosure and actionable guidance.

---

## 1. Skill Folder Structure

```
wxo-dev/
├── SKILL.md                    # Main skill file (condensed guidance)
├── examples.md                 # Complete reference implementations
├── references/
│   ├── project-structure.md    # Detailed project organization
│   ├── yaml-schemas.md         # Agent, tool, KB YAML formats
│   ├── cli-commands.md         # Complete CLI reference
│   └── troubleshooting.md      # Common issues and solutions
├── scripts/
│   ├── import-all.sh           # Template deployment script
│   ├── setup-connection.sh     # Connection setup template
│   └── create-kb.sh            # Knowledge base creation template
└── templates/
    ├── agent-template.yaml     # Agent YAML template
    ├── tool-template.py        # Python tool template
    ├── workflow-template.py    # Agentic workflow template
    ├── kb-template.yaml        # Knowledge base template
    ├── connection-template.yaml # Connection template
    └── .env.example            # Environment configuration template
```

**Rationale:**
- **SKILL.md**: Core guidance (target: 800-1000 lines) - condensed, actionable
- **examples.md**: Complete working examples with full context
- **references/**: Deep-dive documentation for specific topics
- **scripts/**: Ready-to-use automation scripts
- **templates/**: Copy-paste starting points for common artifacts

---

## 2. SKILL.md Frontmatter

```markdown
---
name: watsonx Orchestrate Development
description: |
  Expert guidance for building production-ready watsonx Orchestrate solutions using the ADK.
  Covers agents, tools, workflows, knowledge bases, MCP integration, security, testing, and deployment.
  Follows IBM best practices and official ADK patterns.
---
```

**Key Points:**
- **Name**: Clear, descriptive, matches the domain
- **Description**: Multi-line, covers scope, mentions key capabilities
- **Concise**: Frontmatter should be scannable and informative

---

## 3. SKILL.md Content Organization

### Structure Overview (Progressive Disclosure)

The SKILL.md will be organized into **8 condensed sections** (down from 10 in the rule):

1. **Quick Start & Project Structure** (Sections 1 + 10 combined)
2. **Agent Development** (Section 2 - core patterns)
3. **Tools & Workflows** (Section 2 - tool/workflow specifics)
4. **Knowledge Bases & MCP Integration** (Sections 6 + 6.5 combined)
5. **Security & Connections** (Section 4)
6. **Testing & Evaluation** (Section 3)
7. **Deployment & Channels** (Section 5)
8. **Troubleshooting & Optimization** (Sections 8 + 9 combined)

### Section-by-Section Breakdown

#### Section 1: Quick Start & Project Structure (150 lines)

**Content:**
- Essential directory structure (agents/, tools/, knowledge_bases/, etc.)
- Critical files (import-all.sh, requirements.txt, .env.example)
- Environment configuration (3 auth methods: orchestrate, myibm, custom)
- Quick reference commands (most common CLI operations)

**What to Include:**
- ✅ Core directories and their purpose
- ✅ .env.example structure with all 3 auth methods
- ✅ Top 10 CLI commands
- ✅ Project initialization checklist

**What to Exclude (move to references/):**
- ❌ Detailed explanations of optional env vars
- ❌ Regional configuration details
- ❌ Complete CLI command reference

**Example Structure:**
```markdown
## Quick Start & Project Structure

### Essential Directories
- `agents/` - Agent YAML configurations
- `tools/` - Python tools and flows
- `knowledge_bases/` - KB configurations and documents
[...]

### Environment Setup
Choose ONE authentication method:
1. **watsonx Orchestrate (SaaS/Trial)**
   ```bash
   WO_DEVELOPER_EDITION_SOURCE=orchestrate
   WO_INSTANCE=https://your-instance.watson-orchestrate.ibm.com
   WO_API_KEY=your-api-key
   ```
[...]

### Quick Commands
```bash
# Import agent
orchestrate agents import -f agents/my-agent.yaml

# List tools
orchestrate tools list
[...]
```
```

---

#### Section 2: Agent Development (150 lines)

**Content:**
- Agent naming conventions (snake_case, no spaces)
- Agent YAML structure (spec_version, kind, name, llm, instructions)
- Guidelines vs Instructions (when to use each)
- LLM configuration (default: groq/openai/gpt-oss-120b)
- Multi-agent collaboration patterns

**What to Include:**
- ✅ Naming rules with good/bad examples
- ✅ Complete agent YAML template with annotations
- ✅ Guidelines structure (condition, action, tool)
- ✅ Collaborator handoff patterns
- ✅ 3-5 common agent patterns

**What to Exclude (move to examples.md):**
- ❌ Complete agent examples (those go in examples.md)
- ❌ Detailed guideline patterns (reference in examples.md)

**Example Structure:**
```markdown
## Agent Development

### Naming Conventions
**CRITICAL**: Use snake_case, no spaces, no special characters

✅ Good: `customer_support_agent`, `sales_outreach_agent`
❌ Bad: `customerSupportAgent`, `customer support agent`

### Agent YAML Structure
```yaml
spec_version: v1
kind: native
name: agent_name          # snake_case required
llm: groq/openai/gpt-oss-120b
instructions: |
  General behavior and persona
guidelines:
  - condition: "Specific trigger"
    action: "Specific action"
    tool: "tool_name"     # Only for tools, NOT collaborators
[...]
```
```

---

#### Section 3: Tools & Workflows (200 lines)

**Content:**
- Python tool development (@tool decorator)
- Type hints requirements (critical for schema generation)
- Agentic workflows (deterministic flows)
- When to use workflows vs agents
- Tool import and testing

**What to Include:**
- ✅ @tool decorator syntax and requirements
- ✅ Type hint standards with examples
- ✅ Workflow structure (@flow decorator)
- ✅ Parameter mapping in workflows (map_input)
- ✅ Tool vs workflow decision matrix
- ✅ Common mistakes and fixes

**What to Exclude (move to examples.md):**
- ❌ Complete tool implementations
- ❌ Full workflow examples
- ❌ Test file examples

**Example Structure:**
```markdown
## Tools & Workflows

### Python Tools
**CRITICAL**: Import decorator correctly
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
    return {"status": "success", "data": result}
```

### Type Hints Requirements
- All parameters MUST have explicit type hints
- Return types MUST be specified
- Use `Dict[str, Any]` not `dict`
- Type hints MUST match docstring descriptions
[...]

### Agentic Workflows
**When to Use:**
- Deterministic, fixed sequence processes
- No LLM reasoning needed between steps
- 60% faster, 80% lower cost than agents

**Structure:**
```python
from ibm_watsonx_orchestrate.flow_builder.flows import flow, Flow, START, END

@flow(name="my_workflow", input_schema=Input, output_schema=Output)
def build_workflow(aflow: Flow) -> Flow:
    node = aflow.tool("toolkit:tool_name")
    node.map_input(input_variable="param", expression="flow.input.param")
    aflow.edge(START, node)
    aflow.edge(node, END)
    return aflow
```
[...]
```

---

#### Section 4: Knowledge Bases & MCP Integration (150 lines)

**Content:**
- Knowledge base YAML format (external documents only)
- Supported document formats and size limits
- MCP toolkit YAML format (spec_version: v1, kind: mcp)
- Referencing MCP tools in agents (toolkit:tool_name)
- Import and verification

**What to Include:**
- ✅ KB YAML structure with document references
- ✅ Supported formats (PDF, DOCX, TXT, etc.) with limits
- ✅ MCP toolkit YAML structure
- ✅ Tool reference format (toolkit:tool_name)
- ✅ Common mistakes (inline content, missing prefix)

**What to Exclude (move to examples.md):**
- ❌ Complete KB examples with documents
- ❌ Full MCP server implementations

**Example Structure:**
```markdown
## Knowledge Bases & MCP Integration

### Knowledge Base Format
**CRITICAL**: Documents must be external files, NOT inline content

```yaml
spec_version: v1
kind: knowledge_base
name: kb_name
description: "KB description"
documents:
  - path: document1.pdf    # Relative path
  - path: docs/doc2.txt
vector_index:
  embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

**Supported Formats:**
- PDF (.pdf) - up to 25 MB
- Word (.docx) - up to 25 MB
- Text (.txt) - up to 5 MB
[...]

### MCP Toolkit Format
```yaml
spec_version: v1
kind: mcp
name: toolkit-name
description: "Toolkit description"
command: python3 server.py
env: []
tools:
  - "*"
package_root: .
```

### Referencing MCP Tools
**CRITICAL**: Use full toolkit:tool_name format

```yaml
tools:
  - product-catalog:search_products    # ✅ Correct
  - search_products                     # ❌ Wrong
```
[...]
```

---

#### Section 5: Security & Connections (100 lines)

**Content:**
- Guardrail plugins (pre-invoke, post-invoke)
- Connection types (key_value for API keys)
- Creating connections for external models
- Security best practices

**What to Include:**
- ✅ Guardrail decorator syntax (@tool with kind parameter)
- ✅ Connection creation workflow (add → configure → set-credentials)
- ✅ Security checklist
- ✅ Common connection patterns

**What to Exclude (move to examples.md):**
- ❌ Complete guardrail implementations
- ❌ Full connection scripts

**Example Structure:**
```markdown
## Security & Connections

### Guardrail Plugins
**CRITICAL**: Use correct decorator syntax

```python
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.agent_builder.tools.types import PythonToolKind

@tool(description="Filter content", kind=PythonToolKind.AGENTPREINVOKE)
def content_filter(plugin_context, payload):
    # Pre-invoke logic
    return result
```

### Creating Connections
**For External Model APIs:**
```bash
# 1. Add connection
orchestrate connections add --app-id openai --env draft

# 2. Configure (use key_value for API keys)
orchestrate connections configure --app-id openai --env draft --type team --kind key_value

# 3. Set credentials
orchestrate connections set-credentials --app-id openai --env draft --entries "api_key=$OPENAI_API_KEY"
```

### Security Checklist
- ✅ Never hardcode credentials
- ✅ Use connections for all external APIs
- ✅ Sanitize all inputs
- ✅ Implement guardrails for sensitive operations
[...]
```

---

#### Section 6: Testing & Evaluation (100 lines)

**Content:**
- Testing Python tools (without @tool decorator)
- Evaluation config format (test_paths, auth_config)
- Quick evaluation vs full evaluation
- Red-teaming for security testing

**What to Include:**
- ✅ Test file structure (copy logic without decorator)
- ✅ Evaluation config YAML format
- ✅ Quick-eval command
- ✅ Metrics (auto-computed, not configurable)

**What to Exclude (move to examples.md):**
- ❌ Complete test implementations
- ❌ Full evaluation datasets

**Example Structure:**
```markdown
## Testing & Evaluation

### Testing Python Tools
**CRITICAL**: Test files must NOT import decorated functions

```python
# tests/test_my_tool.py
def my_tool(param: str) -> Dict:
    """Copy business logic from tools/my_tool.py WITHOUT @tool decorator"""
    # Same logic as tool
    return result

def test_success():
    result = my_tool("test")
    assert result['status'] == 'success'
```

### Evaluation Config
```yaml
test_paths:
  - evaluation/datasets/
auth_config:
  url: http://localhost:4321
  tenant_name: local
output_dir: evaluation/results/
enable_verbose_logging: true
```

### Quick Evaluation
```bash
orchestrate evaluations quick-eval -p tests/ -o results/ -t tools/
```

**Metrics** (auto-computed, not configurable):
- Tool Calls, Successful Tool Calls
- Schema Mismatch, Hallucination
- Response/Retrieval Confidence
[...]
```

---

#### Section 7: Deployment & Channels (80 lines)

**Content:**
- Channel types (webchat, slack, teams, etc.)
- Channel configuration
- Deployment process
- Environment-specific configs

**What to Include:**
- ✅ Supported channel types
- ✅ Channel YAML structure
- ✅ Deployment workflow
- ✅ Verification steps

**What to Exclude (move to examples.md):**
- ❌ Complete channel configurations
- ❌ Detailed deployment scripts

**Example Structure:**
```markdown
## Deployment & Channels

### Supported Channels
- webchat (auto-available)
- twilio_whatsapp, twilio_sms
- byo_slack, teams
- genesys_bot_connector

### Channel Configuration
```yaml
name: channel-name
type: slack
agent: agent-name
settings:
  workspace_id: ${SLACK_WORKSPACE_ID}
  bot_token: ${SLACK_BOT_TOKEN}
```

### Deployment Process
```bash
# 1. Import all artifacts
./import-all.sh

# 2. Verify
orchestrate agents list
orchestrate tools list

# 3. Deploy channels
orchestrate channels deploy channel-name
```
[...]
```

---

#### Section 8: Troubleshooting & Optimization (70 lines)

**Content:**
- Common errors and solutions
- Performance optimization tips
- Token usage optimization
- Debugging strategies

**What to Include:**
- ✅ Top 10 common errors with fixes
- ✅ Performance optimization checklist
- ✅ Debugging workflow
- ✅ Log analysis tips

**What to Exclude (move to references/troubleshooting.md):**
- ❌ Exhaustive error catalog
- ❌ Detailed debugging procedures

**Example Structure:**
```markdown
## Troubleshooting & Optimization

### Common Errors

**Error: Tool not found**
```bash
# Verify tool is imported
orchestrate tools list
```

**Error: "required property" in workflow**
```python
# Missing map_input - add parameter mapping
node.map_input(input_variable="param", expression="flow.input.param")
```

### Performance Optimization
- Use workflows for deterministic processes (60% faster)
- Cache frequently accessed data
- Choose appropriate model sizes
- Implement response caching
- Monitor token usage

### Debugging Workflow
1. Test tools independently (without decorator)
2. Verify imports: `orchestrate tools list`
3. Check logs for errors
4. Use quick-eval for validation
[...]
```

---

## 4. examples.md Content Strategy

**Purpose:** Complete, working reference implementations that demonstrate best practices.

**Structure:**

```markdown
# watsonx Orchestrate Development - Examples

## Table of Contents
1. Complete Agent Examples
2. Tool Examples
3. Workflow Examples
4. Knowledge Base Examples
5. MCP Integration Examples
6. Multi-Agent Collaboration Examples
7. Testing Examples
8. Deployment Examples

## 1. Complete Agent Examples

### Customer Support Agent
[Full agent YAML with guidelines, tools, collaborators]

### Sales Agent with Knowledge Base
[Agent using KB for product information]

### Document Processing Agent
[Agent with document handling workflow]

## 2. Tool Examples

### Order Status Tool
[Complete Python tool with type hints, error handling]

### API Integration Tool
[Tool using connections for external API]

### Document Parser Tool
[Tool with file handling and validation]

## 3. Workflow Examples

### Loan Approval Workflow
[Complete workflow with branching, parameter mapping]

### Order Processing Workflow
[Sequential workflow with multiple tools]

### Document Analysis Workflow
[Workflow with foreach and parallel execution]

[... continue for all sections ...]
```

**What Goes in examples.md:**
- ✅ Complete, runnable code examples
- ✅ Full YAML configurations
- ✅ End-to-end implementations
- ✅ Multiple variations of patterns
- ✅ Real-world scenarios
- ✅ Test file examples
- ✅ Deployment scripts

**What Stays in SKILL.md:**
- ✅ Condensed syntax and structure
- ✅ Key concepts and rules
- ✅ Decision matrices
- ✅ Quick reference patterns
- ✅ Common mistakes and fixes

---

## 5. Supporting Files Strategy

### references/project-structure.md
- Detailed directory explanations
- File naming conventions
- Organization best practices
- Monorepo vs multi-repo strategies

### references/yaml-schemas.md
- Complete YAML schema documentation
- All optional parameters
- Advanced configurations
- Schema validation rules

### references/cli-commands.md
- Complete CLI reference
- All commands with all flags
- Advanced usage patterns
- Scripting examples

### references/troubleshooting.md
- Exhaustive error catalog
- Debugging procedures
- Log analysis techniques
- Performance profiling

### scripts/import-all.sh
```bash
#!/bin/bash
set -e

echo "🚀 Importing watsonx Orchestrate artifacts..."

# Import agents
echo "📦 Importing agents..."
for file in agents/*.yaml; do
    orchestrate agents import -f "$file"
done

# Import tools
echo "🔧 Importing tools..."
for file in tools/*.py; do
    orchestrate tools import -k python -f "$file"
done

# Import workflows
echo "🔄 Importing workflows..."
for file in tools/*_workflow.py; do
    orchestrate tools import -k flow -f "$file"
done

# Import knowledge bases
echo "📚 Importing knowledge bases..."
for file in knowledge_bases/*.yaml; do
    orchestrate knowledge-bases import -f "$file"
done

# Import toolkits
echo "🧰 Importing toolkits..."
for file in toolkits/*.yaml; do
    orchestrate toolkits import -f "$file"
done

echo "✅ Import complete!"
```

### scripts/setup-connection.sh
```bash
#!/bin/bash
# Template for setting up external API connections
APP_ID="${1:-my-connection}"
ENV="${2:-draft}"

orchestrate connections add --app-id "$APP_ID" --env "$ENV"
orchestrate connections configure --app-id "$APP_ID" --env "$ENV" --type team --kind key_value
orchestrate connections set-credentials --app-id "$APP_ID" --env "$ENV" --entries "api_key=$API_KEY"
```

### templates/agent-template.yaml
```yaml
spec_version: v1
kind: native
name: agent_name
llm: groq/openai/gpt-oss-120b
style: default

description: |
  Agent description

instructions: |
  Agent instructions and behavior

guidelines:
  - condition: "Trigger condition"
    action: "Action to take"
    tool: "tool_name"

tools: []
collaborators: []
knowledge_base: []
```

### templates/tool-template.py
```python
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from typing import Dict, Any

@tool
def tool_name(param: str) -> Dict[str, Any]:
    """
    Tool description.
    
    Args:
        param (str): Parameter description
        
    Returns:
        Dict[str, Any]: Result description
    """
    try:
        # Tool logic
        result = process(param)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

---

## 6. Progressive Disclosure Strategy

### Level 1: SKILL.md Frontmatter
- Name and description
- Immediate context about what the skill covers

### Level 2: SKILL.md Section Headers
- 8 major sections with clear titles
- Quick scan reveals all topics covered

### Level 3: SKILL.md Section Content
- Condensed, actionable guidance
- Critical rules and patterns
- Common mistakes
- Quick reference syntax

### Level 4: examples.md
- Complete implementations
- Multiple variations
- Real-world scenarios
- Copy-paste ready code

### Level 5: references/
- Deep-dive documentation
- Exhaustive details
- Advanced configurations
- Edge cases

### Level 6: scripts/ and templates/
- Ready-to-use automation
- Starting points for common tasks
- Customizable templates

**Navigation Pattern:**
```
SKILL.md (800-1000 lines)
    ↓
"See examples.md for complete implementations"
    ↓
"See references/yaml-schemas.md for all options"
    ↓
"Use templates/agent-template.yaml as starting point"
```

---

## 7. Content Condensation Strategy

### From Rule to Skill: Reduction Techniques

**Original Rule: 2194 lines**
**Target SKILL.md: 800-1000 lines**
**Reduction: ~55% compression**

#### Technique 1: Remove Redundancy
- Eliminate repeated explanations
- Consolidate similar patterns
- Remove verbose examples from main content

#### Technique 2: Extract to Examples
- Move complete implementations to examples.md
- Keep only syntax and structure in SKILL.md
- Reference examples instead of including them

#### Technique 3: Extract to References
- Move detailed explanations to references/
- Keep only critical rules in SKILL.md
- Link to references for deep dives

#### Technique 4: Consolidate Sections
- Combine related topics (KB + MCP, Troubleshooting + Optimization)
- Reduce from 10 sections to 8
- Focus on workflow-oriented organization

#### Technique 5: Use Tables and Lists
- Replace paragraphs with bullet points
- Use tables for comparisons
- Employ checklists for procedures

#### Technique 6: Emphasize Critical Information
- Use **CRITICAL** markers for must-know items
- ✅/❌ for good/bad examples
- Keep warnings and common mistakes

---

## 8. Quality Metrics

### SKILL.md Success Criteria
- ✅ 800-1000 lines (condensed from 2194)
- ✅ All 10 original areas covered (in 8 sections)
- ✅ Scannable structure (clear headers, lists, tables)
- ✅ Actionable guidance (not just theory)
- ✅ Critical rules highlighted
- ✅ Common mistakes documented
- ✅ Links to examples and references

### examples.md Success Criteria
- ✅ 10+ complete, working examples
- ✅ Covers all major patterns
- ✅ Copy-paste ready code
- ✅ Real-world scenarios
- ✅ Multiple variations per pattern

### Overall Skill Success Criteria
- ✅ Coding agents can build wxO solutions without extensive doc searches
- ✅ Progressive disclosure works (quick start → deep dive)
- ✅ Templates accelerate development
- ✅ Scripts automate common tasks
- ✅ References provide exhaustive details when needed

---

## 9. Implementation Checklist

- [ ] Create skill folder structure
- [ ] Write SKILL.md frontmatter
- [ ] Write SKILL.md Section 1: Quick Start & Project Structure
- [ ] Write SKILL.md Section 2: Agent Development
- [ ] Write SKILL.md Section 3: Tools & Workflows
- [ ] Write SKILL.md Section 4: Knowledge Bases & MCP Integration
- [ ] Write SKILL.md Section 5: Security & Connections
- [ ] Write SKILL.md Section 6: Testing & Evaluation
- [ ] Write SKILL.md Section 7: Deployment & Channels
- [ ] Write SKILL.md Section 8: Troubleshooting & Optimization
- [ ] Create examples.md with 10+ complete examples
- [ ] Create references/project-structure.md
- [ ] Create references/yaml-schemas.md
- [ ] Create references/cli-commands.md
- [ ] Create references/troubleshooting.md
- [ ] Create scripts/import-all.sh
- [ ] Create scripts/setup-connection.sh
- [ ] Create scripts/create-kb.sh
- [ ] Create templates/agent-template.yaml
- [ ] Create templates/tool-template.py
- [ ] Create templates/workflow-template.py
- [ ] Create templates/kb-template.yaml
- [ ] Create templates/connection-template.yaml
- [ ] Create templates/.env.example
- [ ] Review and validate all content
- [ ] Test with coding agent
- [ ] Iterate based on feedback

---

## 10. Next Steps

1. **Review this design document** with stakeholders
2. **Validate the structure** against skill format requirements
3. **Begin implementation** starting with SKILL.md frontmatter and Section 1
4. **Iterate section by section** with validation at each step
5. **Create examples.md** after SKILL.md is complete
6. **Build supporting files** (references, scripts, templates)
7. **Test with coding agents** to validate effectiveness
8. **Refine based on feedback** from real usage

---

## Appendix: Section Size Targets

| Section | Target Lines | Content Focus |
|---------|-------------|---------------|
| 1. Quick Start & Project Structure | 150 | Setup, structure, commands |
| 2. Agent Development | 150 | Naming, YAML, guidelines |
| 3. Tools & Workflows | 200 | @tool, @flow, type hints |
| 4. Knowledge Bases & MCP | 150 | KB format, MCP integration |
| 5. Security & Connections | 100 | Guardrails, connections |
| 6. Testing & Evaluation | 100 | Testing, eval config |
| 7. Deployment & Channels | 80 | Channels, deployment |
| 8. Troubleshooting & Optimization | 70 | Errors, performance |
| **Total** | **1000** | **Condensed guidance** |

---

## Appendix: Content Migration Map

| Original Rule Section | SKILL.md Section | examples.md | references/ | scripts/ | templates/ |
|----------------------|------------------|-------------|-------------|----------|------------|
| 1. Project Structure | Section 1 | ✓ | project-structure.md | import-all.sh | .env.example |
| 2. Development Patterns | Sections 2, 3 | ✓ | yaml-schemas.md | - | agent-template.yaml, tool-template.py |
| 3. Testing & QA | Section 6 | ✓ | - | - | - |
| 4. Security & Guardrails | Section 5 | ✓ | - | setup-connection.sh | connection-template.yaml |
| 5. Deployment & Channels | Section 7 | ✓ | - | - | - |
| 6. MCP Integration | Section 4 | ✓ | - | - | - |
| 6.5. Knowledge Bases | Section 4 | ✓ | - | create-kb.sh | kb-template.yaml |
| 7. Documentation Standards | Sections 2, 3 | ✓ | - | - | - |
| 8. Troubleshooting | Section 8 | - | troubleshooting.md | - | - |
| 9. Performance | Section 8 | - | - | - | - |
| 10. Quick Reference | Section 1 | - | cli-commands.md | - | - |
