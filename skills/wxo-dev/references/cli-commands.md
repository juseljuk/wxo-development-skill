# CLI Commands Reference

Complete reference for watsonx Orchestrate CLI commands.

## Agent Commands

### Import Agent
```bash
orchestrate agents import -f agents/my-agent.yaml
```

### List Agents
```bash
orchestrate agents list
```

### Get Agent Details
```bash
orchestrate agents get -n agent-name
```

### Export Agent
```bash
orchestrate agents export -k native -n agent-name -o agent.zip
```

### Remove Agent
```bash
orchestrate agents remove --name agent-name
```

### Deploy Agent (not in Developer Edition)
```bash
orchestrate agents deploy --name agent-name
```

### Undeploy Agent (not in Developer Edition)
```bash
orchestrate agents undeploy --name agent-name
```

---

## Tool Commands

### Import Python Tool
```bash
orchestrate tools import -k python -f tools/my-tool.py
```

### Import Python Tool with Requirements
```bash
orchestrate tools import -k python -f tools/my-tool.py -r requirements.txt
```

### Import Workflow
```bash
orchestrate tools import -k flow -f tools/my-workflow.py
```

### List Tools
```bash
orchestrate tools list
```

### Get Tool Details
```bash
orchestrate tools get -n tool-name
```

### Remove Tool
```bash
orchestrate tools remove -n tool-name
```

### Export Tool
```bash
orchestrate tools export -n tool-name -o tool.zip
```

---

## Toolkit Commands

### Import Toolkit from YAML
```bash
orchestrate toolkits import -f toolkits/my-toolkit.yaml
```

### Add Toolkit via CLI
```bash
orchestrate toolkits add \
  --kind mcp \
  --name my-toolkit \
  --description "Toolkit description" \
  --package-root ./mcp_server \
  --command "python3 server.py" \
  --tools "*"
```

### List Toolkits
```bash
orchestrate toolkits list
```

### Get Toolkit Details
```bash
orchestrate toolkits get -n toolkit-name
```

### Export Toolkit
```bash
orchestrate toolkits export -n toolkit-name -o toolkit.zip
```

### Remove Toolkit
```bash
orchestrate toolkits remove -n toolkit-name
```

---

## Knowledge Base Commands

### Import Knowledge Base
```bash
orchestrate knowledge-bases import -f knowledge_bases/my-kb.yaml
```

### List Knowledge Bases
```bash
orchestrate knowledge-bases list
```

### Get Knowledge Base Details
```bash
orchestrate knowledge-bases get -n kb-name
```

### Check Knowledge Base Status
```bash
orchestrate knowledge-bases get -n kb-name | grep status
```

### Remove Knowledge Base
```bash
orchestrate knowledge-bases remove -n kb-name
```

---

## Connection Commands

### Add Connection
```bash
orchestrate connections add --app-id connection-name --env draft
orchestrate connections add --app-id connection-name --env live
```

### Configure Connection
```bash
orchestrate connections configure \
  --app-id connection-name \
  --env draft \
  --type team \
  --kind key_value
```

### Set Credentials
```bash
orchestrate connections set-credentials \
  --app-id connection-name \
  --env draft \
  --entries "api_key=$API_KEY"
```

### List Connections
```bash
orchestrate connections list
```

### Get Connection Details
```bash
orchestrate connections get -a connection-name
```

### Import Connection from YAML
```bash
orchestrate connections import -f connections/my-connection.yaml
```

### Export Connection
```bash
orchestrate connections export -a connection-name -o connection.yaml
```

### Remove Connection
```bash
orchestrate connections remove -a connection-name
```

---

## Model Commands

### Add External Model
```bash
orchestrate models add --name provider/model-name --app-id connection-name
```

### List Models
```bash
orchestrate models list
```

### Remove Model
```bash
orchestrate models remove --name provider/model-name
```

---

## Channel Commands

### List Supported Channel Types
```bash
orchestrate channels list
```

### List Channels for Agent
```bash
orchestrate channels list-channels --agent-name my-agent --env draft
```

### Import Channel from File
```bash
orchestrate channels import \
  --agent-name my-agent \
  --env draft \
  --file channels/my-channel.yaml
```

### Export Channel
```bash
orchestrate channels export \
  --agent-name my-agent \
  --env draft \
  --type webchat \
  --name my-channel \
  -o channel.yaml
```

### Delete Channel
```bash
orchestrate channels delete \
  --agent-name my-agent \
  --env draft \
  --type webchat \
  --name my-channel
```

### Deploy Channel
```bash
orchestrate channels deploy channel-name
```

---

## Evaluation Commands

### Quick Evaluation
```bash
orchestrate evaluations quick-eval -p tests/ -o results/ -t tools/
```

### Quick Evaluation with Config
```bash
orchestrate evaluations quick-eval -c evaluation/config.yaml
```

### Standard Evaluation
```bash
orchestrate evaluations evaluate -c evaluation/eval-config.yaml
```

### Red-Teaming: List Attack Types
```bash
orchestrate evaluations red-teaming list
```

### Red-Teaming: Plan Attacks
```bash
orchestrate evaluations red-teaming plan \
  -a "instruction_override,crescendo_attack,jailbreaking" \
  -d evaluation/test-cases.jsonl \
  -g . \
  -t agent_name \
  -o evaluation/red-team-attacks/ \
  -n 3
```

### Red-Teaming: Run Attacks
```bash
orchestrate evaluations red-teaming run \
  -a evaluation/red-team-attacks/ \
  -o evaluation/red-team-results/
```

---

## Environment Commands

### Add Environment
```bash
orchestrate env add --name local --url http://localhost:4321
```

### List Environments
```bash
orchestrate env list
```

### Set Active Environment
```bash
orchestrate env use local
```

### Remove Environment
```bash
orchestrate env remove --name local
```

---

## Utility Commands

### Check Version
```bash
orchestrate --version
```

### Get Help
```bash
orchestrate --help
orchestrate agents --help
orchestrate tools --help
```

### Verbose Output
```bash
orchestrate agents import -f agent.yaml -v
```

---

## Common Command Patterns

### Import All Artifacts
```bash
# Import in correct order
for file in connections/*.yaml; do
    orchestrate connections import -f "$file"
done

for file in toolkits/*.yaml; do
    orchestrate toolkits import -f "$file"
done

for file in tools/*.py; do
    [[ ! "$file" =~ _workflow\.py$ ]] && \
        orchestrate tools import -k python -f "$file"
done

for file in tools/*_workflow.py; do
    orchestrate tools import -k flow -f "$file"
done

for file in knowledge_bases/*.yaml; do
    orchestrate knowledge-bases import -f "$file"
done

for file in agents/*.yaml; do
    orchestrate agents import -f "$file"
done
```

### Verify Imports
```bash
echo "Agents:"
orchestrate agents list

echo "Tools:"
orchestrate tools list

echo "Toolkits:"
orchestrate toolkits list

echo "Knowledge Bases:"
orchestrate knowledge-bases list

echo "Connections:"
orchestrate connections list
```

### Clean Up All Artifacts
```bash
# Remove all agents
orchestrate agents list | grep -v "NAME" | awk '{print $1}' | \
    xargs -I {} orchestrate agents remove --name {}

# Remove all tools
orchestrate tools list | grep -v "NAME" | awk '{print $1}' | \
    xargs -I {} orchestrate tools remove -n {}

# Remove all toolkits
orchestrate toolkits list | grep -v "NAME" | awk '{print $1}' | \
    xargs -I {} orchestrate toolkits remove -n {}

# Remove all knowledge bases
orchestrate knowledge-bases list | grep -v "NAME" | awk '{print $1}' | \
    xargs -I {} orchestrate knowledge-bases remove -n {}
```

### Search for Specific Tool
```bash
orchestrate tools list | grep "search"
```

### Export All Agents
```bash
mkdir -p exports
orchestrate agents list | grep -v "NAME" | awk '{print $1}' | \
    xargs -I {} orchestrate agents export -k native -n {} -o exports/{}.zip
```

---

## Command Options Reference

### Common Flags

- `-f, --file` - File path
- `-n, --name` - Name/identifier
- `-o, --output` - Output file/directory
- `-k, --kind` - Kind/type (python, flow, native, mcp)
- `-v, --verbose` - Verbose output
- `-h, --help` - Show help

### Environment Flags

- `--env` - Environment (draft, live)
- `--url` - Environment URL
- `--tenant-name` - Tenant name

### Connection Flags

- `--app-id` - Connection application ID
- `--type` - Connection type (team, member)
- `--kind` - Connection kind (key_value, api_key, oauth2)
- `--entries` - Credential entries

### Evaluation Flags

- `-p, --test-paths` - Test dataset paths
- `-o, --output-dir` - Output directory
- `-t, --tools-path` - Tools path
- `-c, --config` - Config file path
- `-n, --num-attacks` - Number of attacks

---

## Error Handling

### Common Errors and Solutions

**Error: "Tool not found"**
```bash
# Verify tool is imported
orchestrate tools list

# Re-import if needed
orchestrate tools import -k python -f tools/my-tool.py
```

**Error: "Connection failed"**
```bash
# Check connection exists
orchestrate connections list

# Verify credentials
orchestrate connections get -a connection-name
```

**Error: "Knowledge base not ready"**
```bash
# Check status
orchestrate knowledge-bases get -n kb-name

# Wait for indexing to complete
watch -n 5 'orchestrate knowledge-bases get -n kb-name | grep status'
```

**Error: "Agent deployment failed"**
```bash
# Check agent exists
orchestrate agents list

# Verify all dependencies
orchestrate tools list
orchestrate knowledge-bases list
```

---

## Scripting Best Practices

### Error Handling in Scripts
```bash
#!/bin/bash
set -e  # Exit on error

if ! orchestrate agents import -f agent.yaml; then
    echo "Failed to import agent"
    exit 1
fi
```

### Conditional Execution
```bash
# Only import if file exists
[ -f "agent.yaml" ] && orchestrate agents import -f agent.yaml
```

### Loop with Error Handling
```bash
for file in agents/*.yaml; do
    if [ -f "$file" ]; then
        echo "Importing $file..."
        if orchestrate agents import -f "$file"; then
            echo "✓ Success"
        else
            echo "✗ Failed: $file"
        fi
    fi
done
```

### Parallel Execution
```bash
# Import multiple files in parallel
find tools -name "*.py" -not -name "*_workflow.py" | \
    xargs -P 4 -I {} orchestrate tools import -k python -f {}
```

---

## Advanced Usage

### Using jq for JSON Processing
```bash
# Get agent names as JSON
orchestrate agents list --format json | jq -r '.[].name'

# Filter tools by type
orchestrate tools list --format json | jq '.[] | select(.type=="python")'
```

### Environment Variables
```bash
# Set default environment
export ORCHESTRATE_ENV=local

# Use in commands
orchestrate agents import -f agent.yaml
```

### Piping Commands
```bash
# Count agents
orchestrate agents list | wc -l

# Search and export
orchestrate agents list | grep "support" | awk '{print $1}' | \
    xargs -I {} orchestrate agents export -k native -n {} -o {}.zip