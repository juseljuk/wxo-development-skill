# Project Structure Reference

Detailed guide for organizing watsonx Orchestrate projects.

## Standard Directory Structure

```
project-root/
├── agents/                      # Agent YAML configurations
│   ├── customer-support-agent.yaml
│   ├── sales-agent.yaml
│   └── escalation-agent.yaml
│
├── tools/                       # Python tools and flows
│   ├── check_order_status.py
│   ├── process_refund.py
│   └── loan_approval_workflow.py
│
├── knowledge_bases/             # KB configurations and documents
│   ├── product-catalog-kb.yaml
│   ├── product_catalog.txt
│   ├── faq-kb.yaml
│   └── faq_document.pdf
│
├── models/                      # LLM model configurations
│   └── custom-model-config.yaml
│
├── toolkits/                    # MCP toolkit definitions
│   ├── product-catalog-toolkit.yaml
│   ├── product_catalog_server.py
│   └── weather-toolkit.yaml
│
├── connections/                 # API connections
│   ├── openai-connection.yaml
│   └── external-api-connection.yaml
│
├── channels/                    # Deployment channels
│   ├── slack-channel.yaml
│   ├── teams-channel.yaml
│   └── web-channel.yaml
│
├── plugins/                     # Guardrail and custom plugins
│   ├── content_safety_plugin.py
│   └── pii_filter_plugin.py
│
├── tests/                       # Test cases
│   ├── test_check_order_status.py
│   └── test_process_refund.py
│
├── evaluation/                  # Evaluation datasets
│   ├── config.yaml
│   └── datasets/
│       ├── test_case_1.json
│       └── test_case_2.json
│
├── scripts/                     # Automation scripts
│   ├── import-all.sh
│   ├── setup-connection.sh
│   └── create-kb.sh
│
├── docs/                        # Documentation
│   ├── architecture.md
│   ├── workflows.md
│   └── deployment.md
│
├── import-all.sh                # Main deployment script
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
└── README.md                    # Project documentation
```

## Directory Purposes

### agents/
Contains agent YAML configuration files. Each agent should have:
- Clear, descriptive snake_case name
- Comprehensive instructions
- Well-defined guidelines
- Appropriate tool and collaborator references

**Naming Convention:** `{purpose}_agent.yaml`

### tools/
Contains Python tools and workflow definitions:
- **Python tools:** Individual `.py` files with `@tool` decorator
- **Workflows:** Files ending in `_workflow.py` with `@flow` decorator
- Each tool should be self-contained and well-documented

**Naming Convention:** 
- Tools: `{action}_{object}.py` (e.g., `check_order_status.py`)
- Workflows: `{process}_workflow.py` (e.g., `loan_approval_workflow.py`)

### knowledge_bases/
Contains knowledge base YAML files and associated documents:
- KB YAML files define structure and settings
- Document files (PDF, DOCX, TXT, etc.) contain actual content
- Keep documents in same directory or subdirectories

**Organization:**
```
knowledge_bases/
├── product-catalog-kb.yaml
├── product_catalog.txt
├── policies/
│   ├── policies-kb.yaml
│   ├── refund_policy.pdf
│   └── shipping_policy.pdf
```

### toolkits/
Contains MCP toolkit YAML files and server implementations:
- Toolkit YAML defines MCP server configuration
- Server files implement MCP protocol
- Keep server code in same directory as toolkit YAML

### connections/
Contains connection configuration files:
- Define external API connections
- Use environment variables for credentials
- Never commit actual credentials

### channels/
Contains channel deployment configurations:
- Slack, Teams, Web, etc.
- Environment-specific settings
- Use environment variables for tokens

### plugins/
Contains guardrail and custom plugin implementations:
- Pre-invoke guardrails (content filtering)
- Post-invoke guardrails (PII redaction)
- Custom plugins for specialized behavior

### tests/
Contains test files for tools and workflows:
- Unit tests for individual tools
- Integration tests for workflows
- Test files should NOT import decorated functions

### evaluation/
Contains evaluation configurations and datasets:
- `config.yaml` - Evaluation configuration
- `datasets/` - JSON test case files
- `results/` - Evaluation output (gitignored)

## File Naming Conventions

### Agent Files
- Format: `{purpose}_agent.yaml`
- Use snake_case
- Be descriptive but concise
- Examples:
  - `customer_support_agent.yaml`
  - `sales_outreach_agent.yaml`
  - `document_processor_agent.yaml`

### Tool Files
- Format: `{verb}_{noun}.py`
- Use snake_case
- Action-oriented names
- Examples:
  - `check_order_status.py`
  - `process_refund.py`
  - `calculate_shipping.py`

### Workflow Files
- Format: `{process}_workflow.py`
- Use snake_case
- End with `_workflow`
- Examples:
  - `loan_approval_workflow.py`
  - `order_processing_workflow.py`
  - `document_analysis_workflow.py`

### Knowledge Base Files
- Format: `{topic}-kb.yaml`
- Use kebab-case for YAML
- Descriptive topic names
- Examples:
  - `product-catalog-kb.yaml`
  - `company-policies-kb.yaml`
  - `technical-documentation-kb.yaml`

### Toolkit Files
- Format: `{name}-toolkit.yaml`
- Use kebab-case
- Match server implementation name
- Examples:
  - `product-catalog-toolkit.yaml`
  - `weather-service-toolkit.yaml`
  - `crm-integration-toolkit.yaml`

## Essential Files

### import-all.sh
Main deployment script that imports all artifacts in correct order:
1. Connections (if needed)
2. Models (if external)
3. Toolkits
4. Tools
5. Workflows
6. Knowledge bases
7. Agents
8. Channels

### requirements.txt
Python dependencies for tools and workflows:
- Do NOT include `ibm-watsonx-orchestrate` (platform-managed)
- Include all tool dependencies
- Pin versions for reproducibility
- Example:
  ```
  pydantic==2.5.0
  requests==2.31.0
  python-dateutil==2.8.2
  ```

### .env.example
Environment variable template:
- Include all required variables
- Use placeholder values
- Document each variable
- Never include actual credentials

### .gitignore
Exclude sensitive and generated files:
```
# Environment
.env
.env.local

# Credentials
*.key
*.pem
credentials/

# Results
evaluation/results/
*.log

# Python
__pycache__/
*.pyc
.venv/
venv/

# IDE
.vscode/
.idea/
```

### README.md
Project documentation should include:
- Project overview
- Architecture diagrams
- Setup instructions
- Usage examples
- Deployment guide
- Troubleshooting tips

## Organization Strategies

### Monorepo vs Multi-repo

**Monorepo (Recommended for most projects):**
- All agents, tools, and resources in one repository
- Easier to maintain consistency
- Simpler deployment
- Better for small to medium projects

**Multi-repo:**
- Separate repositories for different components
- Better for large, complex systems
- Independent versioning
- More complex deployment

### Environment-Specific Organization

For projects with multiple environments:

```
project-root/
├── agents/
│   ├── base/                    # Shared agent configs
│   ├── dev/                     # Dev-specific overrides
│   ├── staging/                 # Staging-specific
│   └── prod/                    # Production-specific
```

### Domain-Driven Organization

For large projects with multiple domains:

```
project-root/
├── customer-service/
│   ├── agents/
│   ├── tools/
│   └── knowledge_bases/
├── sales/
│   ├── agents/
│   ├── tools/
│   └── knowledge_bases/
└── operations/
    ├── agents/
    ├── tools/
    └── knowledge_bases/
```

## Best Practices

### Version Control
- Commit all configuration files
- Never commit credentials or .env files
- Use meaningful commit messages
- Tag releases for deployment tracking

### Documentation
- Document all agents, tools, and workflows
- Include architecture diagrams
- Maintain changelog
- Document deployment procedures

### Testing
- Test tools independently before integration
- Create evaluation datasets for agents
- Run evaluations before deployment
- Document test procedures

### Security
- Use connections for all external APIs
- Implement appropriate guardrails
- Regular security audits
- Follow least privilege principle

### Maintenance
- Regular dependency updates
- Monitor performance metrics
- Review and update documentation
- Periodic code reviews