# Troubleshooting Guide

Comprehensive guide for diagnosing and resolving common issues.

## Common Errors

### Import Errors

#### Error: "Tool not found"
**Symptom:** Agent references a tool that doesn't exist

**Diagnosis:**
```bash
# Check if tool is imported
orchestrate tools list | grep tool-name
```

**Solutions:**
1. Import the tool:
   ```bash
   orchestrate tools import -k python -f tools/my-tool.py
   ```

2. Verify tool name matches decorator:
   ```python
   @tool
   def my_tool(...):  # Name must match reference
   ```

3. For MCP tools, verify toolkit prefix:
   ```yaml
   tools:
     - toolkit:tool_name  # Not just tool_name
   ```

#### Error: "Agent not found"
**Symptom:** Collaborator or channel references non-existent agent

**Diagnosis:**
```bash
orchestrate agents list | grep agent-name
```

**Solutions:**
1. Import the agent first:
   ```bash
   orchestrate agents import -f agents/agent-name.yaml
   ```

2. Check agent name spelling in YAML

3. Verify agent name is snake_case

#### Error: "Knowledge base not found"
**Symptom:** Agent references KB that doesn't exist

**Diagnosis:**
```bash
orchestrate knowledge-bases list | grep kb-name
```

**Solutions:**
1. Import the knowledge base:
   ```bash
   orchestrate knowledge-bases import -f knowledge_bases/kb.yaml
   ```

2. Wait for indexing to complete:
   ```bash
   orchestrate knowledge-bases get -n kb-name
   # Status should be "ready"
   ```

3. Verify KB name matches exactly in agent YAML

---

### Runtime Errors

#### Error: "Agent timeout"
**Symptom:** Agent takes too long to respond

**Diagnosis:**
- Check tool execution times
- Review LLM response times
- Analyze conversation context size

**Solutions:**
1. Optimize tool execution:
   ```python
   @tool
   def my_tool(param: str) -> Dict[str, Any]:
       # Add timeout
       result = requests.get(url, timeout=5)
       return {"status": "success", "data": result}
   ```

2. Reduce context size:
   - Implement conversation summarization
   - Limit knowledge base results
   - Use concise instructions

3. Use faster LLM model:
   ```yaml
   llm: groq/openai/gpt-oss-120b  # Faster than larger models
   ```

#### Error: "Token limit exceeded"
**Symptom:** Request exceeds model's token limit

**Diagnosis:**
- Check conversation history length
- Review instruction size
- Analyze knowledge base retrieval

**Solutions:**
1. Reduce instruction length:
   ```yaml
   instructions: |
     Be concise. Focus on key points.
   ```

2. Limit KB results:
   ```yaml
   conversational_search_tool:
     generation:
       max_docs_passed_to_llm: 5  # Reduce from 10
   ```

3. Implement conversation summarization

4. Use model with larger context window

#### Error: "Connection failed"
**Symptom:** Tool can't connect to external API

**Diagnosis:**
```bash
# Check connection exists
orchestrate connections list

# Verify credentials
orchestrate connections get -a connection-name
```

**Solutions:**
1. Verify connection is configured:
   ```bash
   orchestrate connections configure \
     --app-id connection-name \
     --env draft \
     --type team \
     --kind key_value
   ```

2. Check credentials are set:
   ```bash
   orchestrate connections set-credentials \
     --app-id connection-name \
     --env draft \
     --entries "api_key=$API_KEY"
   ```

3. Test connection in tool:
   ```python
   try:
       response = requests.get(url, headers=headers, timeout=10)
       response.raise_for_status()
   except requests.exceptions.RequestException as e:
       return {"status": "error", "message": f"Connection failed: {str(e)}"}
   ```

---

### Workflow Errors

#### Error: "Required property missing"
**Symptom:** Workflow tool receives empty/missing parameters

**Diagnosis:**
- Verify tool parameter names match data sources
- Check input schema field names
- Review expression references in evaluators

**Solutions:**
1. Ensure parameter name consistency:
   ```python
   # Workflow input schema
   class WorkflowInput(BaseModel):
       customer_id: str = Field(description="Customer identifier")
   
   # Tool will automatically receive customer_id from flow.input.customer_id
   # if the tool's parameter is named "customer_id"
   node = aflow.tool("toolkit:tool_name")
   ```

2. Verify data source references:
   ```python
   # Tool automatically receives data from:
   # - Workflow inputs: flow.input.param_name
   # - Previous node outputs: node_name.output.field_name
   # No explicit mapping code needed - automatic runtime resolution
   ```

3. Check input schema matches tool expectations:
   ```python
   class WorkflowInput(BaseModel):
       # Field names must match what tools expect
       customer_id: str = Field(description="Customer identifier")
       amount: float = Field(description="Transaction amount")
   ```

**Note:** watsonx Orchestrate uses automatic runtime data mapping. Tools receive data automatically when parameter names match workflow inputs or previous node outputs. No explicit mapping code is needed.

#### Error: "Tool not found in workflow"
**Symptom:** Workflow can't find referenced tool

**Diagnosis:**
```bash
# Verify tool exists with toolkit prefix
orchestrate tools list | grep toolkit-name
```

**Solutions:**
1. Use full toolkit:tool_name format:
   ```python
   node = aflow.tool("loan-processing:check_credit")  # Not just "check_credit"
   ```

2. Import toolkit before workflow:
   ```bash
   orchestrate toolkits import -f toolkits/my-toolkit.yaml
   orchestrate tools import -k flow -f tools/my-workflow.py
   ```

#### Error: "Workflow import failed"
**Symptom:** Can't import workflow as flow-type tool

**Diagnosis:**
- Check import command uses `-k flow`
- Verify @flow decorator syntax
- Review input/output schemas

**Solutions:**
1. Use correct import command:
   ```bash
   orchestrate tools import -k flow -f tools/my-workflow.py
   ```

2. Verify @flow decorator:
   ```python
   @flow(
       name="workflow_name",
       description="Description",
       input_schema=InputModel,
       output_schema=OutputModel
   )
   ```

3. Check Pydantic models are valid:
   ```python
   from pydantic import BaseModel, Field
   
   class Input(BaseModel):
       param: str = Field(description="Desc")
   ```

---

### Knowledge Base Errors

#### Error: "Document not found"
**Symptom:** KB import fails due to missing document

**Diagnosis:**
- Check document path in YAML
- Verify file exists
- Review path relativity

**Solutions:**
1. Use correct relative path:
   ```yaml
   documents:
     - path: product_catalog.txt  # Same directory as YAML
     - path: docs/faq.pdf          # Subdirectory
   ```

2. Verify file exists:
   ```bash
   ls -la knowledge_bases/product_catalog.txt
   ```

3. Check file permissions:
   ```bash
   chmod 644 knowledge_bases/product_catalog.txt
   ```

#### Error: "Knowledge base not ready"
**Symptom:** Agent can't use KB because it's still indexing

**Diagnosis:**
```bash
orchestrate knowledge-bases get -n kb-name | grep status
```

**Solutions:**
1. Wait for indexing to complete:
   ```bash
   # Check status periodically
   watch -n 5 'orchestrate knowledge-bases get -n kb-name | grep status'
   ```

2. For large documents, indexing may take several minutes

3. If stuck, re-import:
   ```bash
   orchestrate knowledge-bases remove -n kb-name
   orchestrate knowledge-bases import -f knowledge_bases/kb.yaml
   ```

#### Error: "Poor retrieval quality"
**Symptom:** KB returns irrelevant results

**Diagnosis:**
- Review chunk size and overlap
- Check document structure
- Analyze query patterns

**Solutions:**
1. Adjust chunking parameters:
   ```yaml
   vector_index:
     chunk_size: 600        # Increase for more context
     chunk_overlap: 100     # Increase for better continuity
   ```

2. Improve document structure:
   - Add clear section headers
   - Use consistent formatting
   - Include relevant keywords

3. Enable query rewriting:
   ```yaml
   conversational_search_tool:
     query_rewrite:
       enabled: true
   ```

4. Lower confidence thresholds:
   ```yaml
   confidence_thresholds:
     retrieval_confidence_threshold: Low
     response_confidence_threshold: Low
   ```

---

### Type Hint Errors

#### Warning: "Unable to parse parameter descriptions"
**Symptom:** Tool schema generation warning

**Diagnosis:**
- Check if type hints are missing
- Verify type hints match docstring
- Review import statements

**Solutions:**
1. Add explicit type hints:
   ```python
   # Wrong
   def my_tool(param):
   
   # Correct
   def my_tool(param: str) -> Dict[str, Any]:
   ```

2. Use specific types:
   ```python
   # Wrong
   def my_tool(data: dict) -> Dict:
   
   # Correct
   from typing import Dict, Any
   def my_tool(data: Dict[str, Any]) -> Dict[str, Any]:
   ```

3. Match docstring types:
   ```python
   @tool
   def my_tool(count: int) -> Dict[str, Any]:  # Type hint: int
       """
       Args:
           count (int): Number of items  # Docstring: int
       """
   ```

---

### Guardrail Errors

#### Error: "Plugin not found"
**Symptom:** Agent references non-existent plugin

**Diagnosis:**
```bash
orchestrate tools list | grep plugin-name
```

**Solutions:**
1. Import plugin before agent:
   ```bash
   orchestrate tools import -k python -f plugins/my-plugin.py
   orchestrate agents import -f agents/my-agent.yaml
   ```

2. Verify plugin decorator syntax:
   ```python
   @tool(description="Plugin description", kind=PythonToolKind.AGENTPREINVOKE)
   def my_plugin(...):
   ```

3. Check plugin name in agent YAML:
   ```yaml
   plugins:
     agent_pre_invoke:
       - plugin_name: my_plugin  # Must match function name
   ```

#### Error: "Plugin execution failed"
**Symptom:** Guardrail plugin crashes

**Diagnosis:**
- Check plugin logs
- Review error messages
- Test plugin independently

**Solutions:**
1. Add error handling:
   ```python
   @tool(description="Plugin", kind=PythonToolKind.AGENTPREINVOKE)
   def my_plugin(plugin_context, payload):
       try:
           # Plugin logic
           return result
       except Exception as e:
           # Log error and allow through
           result = AgentPreInvokeResult()
           result.continue_processing = True
           result.modified_payload = payload
           return result
   ```

2. Validate payload structure:
   ```python
   if not payload or not payload.messages:
       result.continue_processing = True
       result.modified_payload = payload
       return result
   ```

---

### Testing Errors

#### Error: "Decorated function returns wrong format"
**Symptom:** Test fails when importing decorated tool

**Diagnosis:**
- Check if test imports decorated function
- Review @tool decorator behavior

**Solutions:**
1. Create test version without decorator:
   ```python
   # tests/test_my_tool.py
   def my_tool(param: str) -> Dict:
       """Copy logic from tools/my_tool.py WITHOUT @tool"""
       # Same business logic
       return result
   ```

2. Don't import from tools/:
   ```python
   # Wrong
   from tools.my_tool import my_tool
   
   # Correct
   # Copy function definition to test file
   ```

#### Error: "Evaluation config invalid"
**Symptom:** Quick-eval fails with config error

**Diagnosis:**
- Check config file format
- Verify required fields
- Review parameter names

**Solutions:**
1. Use correct config structure:
   ```yaml
   test_paths:           # Not dataset_path
     - evaluation/datasets/
   auth_config:
     url: http://localhost:4321
     tenant_name: local
   output_dir: evaluation/results/
   ```

2. Don't configure metrics:
   ```yaml
   # Wrong - metrics are auto-computed
   metrics:
     - response_confidence
   
   # Correct - no metrics section needed
   ```

3. Use correct tenant name:
   ```yaml
   auth_config:
     tenant_name: local  # Must match orchestrate env add
   ```

---

## Debugging Strategies

### 1. Test Tools Independently

```python
# test_tool_standalone.py
from tools.my_tool import my_tool

# Test without decorator
result = my_tool("test_input")
print(result)
```

### 2. Enable Verbose Logging

```bash
orchestrate agents import -f agent.yaml -v
```

### 3. Check Logs

```bash
# View agent execution logs
tail -f ~/.orchestrate/logs/agent.log

# Search for errors
grep ERROR ~/.orchestrate/logs/*.log
```

### 4. Verify Dependencies

```bash
# Check all artifacts exist
echo "Agents:"
orchestrate agents list

echo "Tools:"
orchestrate tools list

echo "Toolkits:"
orchestrate toolkits list

echo "Knowledge Bases:"
orchestrate knowledge-bases list
```

### 5. Test in Isolation

```bash
# Test single agent
orchestrate agents import -f agents/test-agent.yaml

# Test single tool
orchestrate tools import -k python -f tools/test-tool.py
```

---

## Performance Issues

### Slow Agent Response

**Diagnosis:**
- Monitor response times
- Check tool execution duration
- Review LLM latency

**Solutions:**
1. Use workflows for deterministic processes (60% faster)
2. Implement caching for repeated operations
3. Optimize tool code
4. Use faster LLM models
5. Reduce context size

### High Token Usage

**Diagnosis:**
- Track token consumption
- Analyze conversation length
- Review instruction size

**Solutions:**
1. Use concise instructions
2. Implement conversation summarization
3. Limit KB retrieval results
4. Choose appropriate model size

### Memory Issues

**Diagnosis:**
- Monitor memory usage
- Check for memory leaks
- Review data structures

**Solutions:**
1. Implement streaming for large data
2. Use generators instead of lists
3. Clear caches periodically
4. Optimize data structures

---

## Getting Help

### Check Documentation
```bash
orchestrate --help
orchestrate agents --help
orchestrate tools --help
```

### Search Logs
```bash
grep -r "ERROR" ~/.orchestrate/logs/
```

### Verify Installation
```bash
orchestrate --version
python --version
```

### Test Connectivity
```bash
# Test local environment
curl http://localhost:4321/health

# Test SaaS environment
curl https://api.watson-orchestrate.ibm.com/health