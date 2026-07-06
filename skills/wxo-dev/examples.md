# watsonx Orchestrate Development - Examples

Complete, working reference implementations demonstrating best practices.

## Table of Contents

1. [Complete Agent Examples](#complete-agent-examples)
2. [Tool Examples](#tool-examples)
3. [Workflow Examples](#workflow-examples)
4. [Knowledge Base Examples](#knowledge-base-examples)
5. [MCP Integration Examples](#mcp-integration-examples)
6. [Multi-Agent Collaboration Examples](#multi-agent-collaboration-examples)
7. [Guardrail Examples](#guardrail-examples)
8. [Testing Examples](#testing-examples)
9. [Connection Examples](#connection-examples)
10. [Deployment Examples](#deployment-examples)

---

## Complete Agent Examples

### Example 1: Customer Support Agent with Guidelines

```yaml
# agents/customer-support-agent.yaml
spec_version: v1
kind: native
name: customer_support_agent
llm: groq/openai/gpt-oss-120b
style: default

description: |
  Handles customer support inquiries including order status checks,
  refund requests, and product information.

instructions: |
  You are a professional customer support agent.
  Always be empathetic and solution-focused.

guidelines:
  - condition: "The customer requests a refund under $500"
    action: "Process immediately and confirm 5-7 day timeline"
    tool: "process_refund"
  
  - condition: "The customer requests a refund over $10,000"
    action: "Hand off to the escalation_agent collaborator for specialist review"
  
  - condition: "The customer mentions legal action"
    action: "Remain professional and hand off to the escalation_agent collaborator"
  
  - condition: "The customer asks about order status"
    action: "Request order ID if not provided, then check status"
    tool: "check_order_status"

tools:
  - check_order_status
  - process_refund

collaborators:
  - escalation_agent

restrictions: editable
```

### Example 2: Sales Agent with Knowledge Base

```yaml
# agents/sales-agent.yaml
spec_version: v1
kind: native
name: sales_outreach_agent
llm: groq/openai/gpt-oss-120b

description: Sales agent using product catalog knowledge base

instructions: |
  You are a knowledgeable sales agent.
  Help customers find the right products for their needs.
  Use the product catalog knowledge base for accurate information.

guidelines:
  - condition: "The customer asks about product specifications"
    action: "Search the product catalog knowledge base for detailed information"
  
  - condition: "The customer asks about availability"
    action: "Use the check_inventory tool"
    tool: "check_inventory"
  
  - condition: "The customer is ready to purchase"
    action: "Hand off to the order_processing_agent collaborator"

tools:
  - check_inventory

collaborators:
  - order_processing_agent

knowledge_base:
  - product_catalog_kb
```

---

## Tool Examples

### Example 1: Order Status Tool

```python
# tools/check_order_status.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from typing import Dict, Any

@tool
def check_order_status(order_id: str) -> Dict[str, Any]:
    """
    Check the status of a customer order.
    
    Args:
        order_id (str): The unique order identifier (format: ORD-XXXXX)
        
    Returns:
        Dict[str, Any]: Order status information
    """
    try:
        if not order_id.startswith("ORD-"):
            return {
                "status": "error",
                "message": "Invalid order ID format. Expected: ORD-XXXXX"
            }
        
        # Simulate database lookup
        order_data = {
            "order_id": order_id,
            "status": "shipped",
            "estimated_delivery": "2024-01-15",
            "tracking_number": "1Z999AA10123456784",
            "items": [{"product": "UltraBook Pro 15", "quantity": 1}]
        }
        
        return {"status": "success", "data": order_data}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

### Example 2: Refund Processing Tool

```python
# tools/process_refund.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from typing import Dict, Any
from datetime import datetime

@tool
def process_refund(order_id: str, amount: float, reason: str) -> Dict[str, Any]:
    """
    Process a customer refund request.
    
    Args:
        order_id (str): The order identifier
        amount (float): The refund amount in USD
        reason (str): The reason for the refund
        
    Returns:
        Dict[str, Any]: Refund processing result
    """
    try:
        if amount > 10000:
            return {
                "status": "error",
                "message": "Refunds over $10,000 require specialist approval"
            }
        
        refund_id = f"REF-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        return {
            "status": "success",
            "message": f"Refund approved. ID: {refund_id}",
            "data": {
                "refund_id": refund_id,
                "order_id": order_id,
                "amount": amount,
                "processing_time": "5-7 business days"
            }
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

---

## Workflow Examples

### Example: Loan Approval Workflow

```python
# tools/loan_approval_workflow.py
from ibm_watsonx_orchestrate.flow_builder.flows import Flow, flow, START, END, Branch
from pydantic import BaseModel, Field
from typing import Dict, Any

class LoanInput(BaseModel):
    applicant_id: str = Field(description="Applicant identifier")
    loan_amount: float = Field(description="Requested amount")
    credit_score: int = Field(description="Credit score (300-850)")

class LoanOutput(BaseModel):
    status: str = Field(description="Approval status")
    loan_amount: float = Field(description="Approved amount")
    interest_rate: float = Field(description="Interest rate")

@flow(
    name="loan_approval_workflow",
    description="Automated loan approval with credit check and risk assessment",
    input_schema=LoanInput,
    output_schema=LoanOutput
)
def build_loan_approval_workflow(aflow: Flow) -> Flow:
    """
    Build loan approval workflow with credit check and risk assessment.
    
    NOTE: watsonx Orchestrate uses automatic runtime data mapping.
    Tools receive data automatically when parameter names match:
    - Workflow inputs (e.g., flow.input.applicant_id)
    - Previous node outputs (e.g., check_credit.output.score)
    
    No explicit mapping code needed - the platform handles this at runtime.
    """
    # Check credit score
    # Tool will automatically receive: applicant_id from flow.input.applicant_id
    check_credit = aflow.tool("loan-processing:check_credit_score")
    
    # Assess risk
    # Tool will automatically receive:
    # - credit_score from check_credit.output.score
    # - loan_amount from flow.input.loan_amount
    assess_risk = aflow.tool("loan-processing:assess_risk")
    
    # Decision branch based on credit score
    credit_branch: Branch = aflow.branch(
        evaluator="check_credit.output.score >= 700"
    )
    
    # Approval node
    # Tool will automatically receive: applicant_id from flow.input.applicant_id
    approve_loan = aflow.tool("loan-processing:approve_loan")
    
    # Rejection node
    # Tool will automatically receive: applicant_id from flow.input.applicant_id
    reject_loan = aflow.tool("loan-processing:reject_loan")
    
    # Build graph
    aflow.edge(START, check_credit)
    aflow.edge(check_credit, assess_risk)
    aflow.edge(assess_risk, credit_branch)
    credit_branch.case(True, approve_loan)
    credit_branch.case(False, reject_loan)
    aflow.edge(approve_loan, END)
    aflow.edge(reject_loan, END)
    
    return aflow
```

---

## Knowledge Base Examples

### Example: Product Catalog Knowledge Base

**Directory Structure:**
```
knowledge_bases/
├── product-catalog-kb.yaml
└── product_catalog.txt
```

**Knowledge Base YAML:**
```yaml
# knowledge_bases/product-catalog-kb.yaml
spec_version: v1
kind: knowledge_base
name: product_catalog_kb
description: |
  Product catalog with specifications, pricing, and availability

documents:
  - path: product_catalog.txt

vector_index:
  embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
  chunk_size: 400
  chunk_overlap: 50

conversational_search_tool:
  generation:
    prompt_instruction: |
      Answer questions about products based on the catalog.
      Provide detailed specifications and pricing.
    max_docs_passed_to_llm: 10
    generated_response_length: Moderate
    idk_message: "I don't have information about that product."
  confidence_thresholds:
    retrieval_confidence_threshold: Low
    response_confidence_threshold: Low
  query_rewrite:
    enabled: true
```

**Document (product_catalog.txt):**
```
PRODUCT CATALOG

PRODUCT 1: UltraBook Pro 15
SKU: UBP-15-2024
Price: $1,899.99
Category: Laptops

Description: Premium laptop for professionals

Specifications:
- Processor: Intel Core i7-13700H
- RAM: 32GB DDR5
- Storage: 1TB NVMe SSD
- Display: 15.6" 4K OLED
- Battery: Up to 12 hours

Availability: In Stock
Shipping: Free 2-day shipping
```

---

## MCP Integration Examples

### Example: Product Catalog MCP Server

**Toolkit YAML:**
```yaml
# toolkits/product-catalog-toolkit.yaml
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

**MCP Server:**
```python
# product_catalog_server.py
import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

PRODUCTS = {
    "UBP-15-2024": {
        "name": "UltraBook Pro 15",
        "price": 1899.99,
        "in_stock": True
    }
}

app = Server("product-catalog")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="search_products",
            description="Search for products",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments):
    if name == "search_products":
        query = arguments.get("query", "").lower()
        results = [p for p in PRODUCTS.values() if query in p["name"].lower()]
        return [TextContent(type="text", text=json.dumps(results))]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

**Agent Using MCP Tools:**
```yaml
# agents/product-agent.yaml
spec_version: v1
kind: native
name: product_assistant
llm: groq/openai/gpt-oss-120b

tools:
  - product-catalog:search_products  # Note: toolkit:tool_name format

guidelines:
  - condition: "Customer searches for products"
    tool: "product-catalog:search_products"
```

---

## Multi-Agent Collaboration Examples

### Example: Support with Escalation

**Main Agent:**
```yaml
# agents/customer-support-agent.yaml
spec_version: v1
kind: native
name: customer_support_agent
llm: groq/openai/gpt-oss-120b

guidelines:
  - condition: "Customer mentions legal action"
    action: "Hand off to escalation_agent collaborator"
  
  - condition: "Refund over $10,000"
    action: "Hand off to escalation_agent collaborator"

tools:
  - check_order_status

collaborators:
  - escalation_agent
```

**Escalation Agent:**
```yaml
# agents/escalation-agent.yaml
spec_version: v1
kind: native
name: escalation_agent
llm: groq/openai/gpt-oss-120b

description: Handles escalated issues

tools:
  - process_high_value_refund
  - notify_management
```

---

## Guardrail Examples

### Example 1: Content Safety Pre-invoke

```python
# plugins/content_safety_plugin.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.agent_builder.tools.types import (
    PythonToolKind,
    PluginContext,
    AgentPreInvokePayload,
    AgentPreInvokeResult,
    TextContent,
    Message
)

@tool(description="Filters inappropriate content", kind=PythonToolKind.AGENTPREINVOKE)
def content_safety_guardrail(plugin_context: PluginContext,
                             agent_pre_invoke_payload: AgentPreInvokePayload) -> AgentPreInvokeResult:
    """Check for inappropriate content before processing."""
    result = AgentPreInvokeResult()
    
    if not agent_pre_invoke_payload or not agent_pre_invoke_payload.messages:
        result.continue_processing = True
        result.modified_payload = agent_pre_invoke_payload
        return result
    
    last_message = agent_pre_invoke_payload.messages[-1]
    content = getattr(last_message, "content", None)
    
    if content and hasattr(content, "text") and content.text:
        user_message = content.text.lower()
        
        # Check for inappropriate content
        if "inappropriate" in user_message:  # Replace with actual checks
            new_text = "I cannot process this request as it violates content guidelines."
            new_content = TextContent(type="text", text=new_text)
            new_message = Message(role=last_message.role, content=new_content)
            
            modified_payload = agent_pre_invoke_payload.copy(deep=True)
            modified_payload.messages[-1] = new_message
            
            result.continue_processing = False
            result.modified_payload = modified_payload
            return result
    
    result.continue_processing = True
    result.modified_payload = agent_pre_invoke_payload
    return result
```

### Example 2: PII Redaction Post-invoke

```python
# plugins/pii_filter_plugin.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.agent_builder.tools.types import (
    PythonToolKind,
    AgentPostInvokePayload,
    AgentPostInvokeResult,
    TextContent,
    Message
)
import re

@tool(description="Redacts PII from responses", kind=PythonToolKind.AGENTPOSTINVOKE)
def pii_filter_guardrail(plugin_context,
                        agent_post_invoke_payload: AgentPostInvokePayload) -> AgentPostInvokeResult:
    """Redact PII from agent responses."""
    result = AgentPostInvokeResult()
    
    if not agent_post_invoke_payload or not agent_post_invoke_payload.messages:
        result.continue_processing = False
        return result
    
    first_msg = agent_post_invoke_payload.messages[0]
    content = getattr(first_msg, "content", None)
    
    if content and hasattr(content, "text") and content.text:
        response_text = content.text
        
        # Redact PII patterns
        response_text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN REDACTED]', response_text)
        response_text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL REDACTED]', response_text)
        
        new_content = TextContent(type="text", text=response_text)
        new_message = Message(role=first_msg.role, content=new_content)
        
        modified_payload = agent_post_invoke_payload.copy(deep=True)
        modified_payload.messages[0] = new_message
        
        result.continue_processing = True
        result.modified_payload = modified_payload
        return result
    
    result.continue_processing = False
    return result
```

---

## Testing Examples

### Example: Testing Python Tools

```python
# tests/test_check_order_status.py
"""
Test cases for check_order_status tool.

Note: Copy tool logic WITHOUT @tool decorator for testing.
"""
from typing import Dict, Any

def check_order_status(order_id: str) -> Dict[str, Any]:
    """Test version without @tool decorator."""
    try:
        if not order_id.startswith("ORD-"):
            return {
                "status": "error",
                "message": "Invalid order ID format"
            }
        
        order_data = {
            "order_id": order_id,
            "status": "shipped"
        }
        
        return {"status": "success", "data": order_data}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

def test_valid_order():
    result = check_order_status("ORD-12345")
    assert result['status'] == 'success'
    assert result['data']['order_id'] == "ORD-12345"
    print("✓ Valid order test passed")

def test_invalid_format():
    result = check_order_status("INVALID")
    assert result['status'] == 'error'
    print("✓ Invalid format test passed")

if __name__ == "__main__":
    test_valid_order()
    test_invalid_format()
```

### Example: Evaluation Config

```yaml
# evaluation/config.yaml
test_paths:
  - evaluation/datasets/

auth_config:
  url: http://localhost:4321
  tenant_name: local

output_dir: evaluation/results/
enable_verbose_logging: true
n_runs: 1
```

---

## Connection Examples

### Example: OpenAI Connection Script

```bash
#!/bin/bash
# scripts/setup-openai-connection.sh
set -e

APP_ID="openai"

if [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: OPENAI_API_KEY not set"
    exit 1
fi

# Draft environment
orchestrate connections add --app-id "$APP_ID" --env draft
orchestrate connections configure --app-id "$APP_ID" --env draft --type team --kind key_value
orchestrate connections set-credentials --app-id "$APP_ID" --env draft --entries "api_key=$OPENAI_API_KEY"

# Live environment
orchestrate connections add --app-id "$APP_ID" --env live
orchestrate connections configure --app-id "$APP_ID" --env live --type team --kind key_value
orchestrate connections set-credentials --app-id "$APP_ID" --env live --entries "api_key=$OPENAI_API_KEY"

echo "✓ OpenAI connection created"

# Import model
orchestrate models add --name openai/gpt-4 --app-id "$APP_ID"
echo "✓ Model imported"
```

---

## Deployment Examples

### Example: Complete Import Script

```bash
#!/bin/bash
# import-all.sh
set -e

echo "🚀 Importing watsonx Orchestrate artifacts..."

# Import agents
echo "📦 Importing agents..."
for file in agents/*.yaml; do
    [ -f "$file" ] && orchestrate agents import -f "$file"
done

# Import Python tools
echo "🔧 Importing Python tools..."
for file in tools/*.py; do
    [ -f "$file" ] && [[ ! "$file" =~ _workflow\.py$ ]] && \
        orchestrate tools import -k python -f "$file"
done

# Import workflows
echo "🔄 Importing workflows..."
for file in tools/*_workflow.py; do
    [ -f "$file" ] && orchestrate tools import -k flow -f "$file"
done

# Import knowledge bases
echo "📚 Importing knowledge bases..."
for file in knowledge_bases/*.yaml; do
    [ -f "$file" ] && orchestrate knowledge-bases import -f "$file"
done

# Import toolkits
echo "🧰 Importing toolkits..."
for file in toolkits/*.yaml; do
    [ -f "$file" ] && orchestrate toolkits import -f "$file"
done

echo "✅ Import complete!"
echo ""
echo "Verify with:"
echo "  orchestrate agents list"
echo "  orchestrate tools list"
echo "  orchestrate knowledge-bases list"
```

### Example: Channel Configuration

```yaml
# channels/slack-channel.yaml
name: customer-support-slack
type: slack
agent: customer_support_agent
settings:
  workspace_id: ${SLACK_WORKSPACE_ID}
  bot_token: ${SLACK_BOT_TOKEN}
```

**Import Channel:**
```bash
orchestrate channels import \
  --agent-name customer_support_agent \
  --env draft \
  --file channels/slack-channel.yaml