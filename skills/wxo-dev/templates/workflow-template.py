"""
Agentic Workflow Template for watsonx Orchestrate

This template demonstrates how to build deterministic, predefined sequences of tool
executions. Workflows are 60% faster and 80% lower cost than agent-based approaches
for predictable processes.

IMPORTANT: watsonx Orchestrate uses automatic runtime data mapping. Tools automatically
receive data based on their parameter names matching the expression references in the
workflow graph. No manual input mapping is required.

Documentation: https://developer.watson-orchestrate.ibm.com/agentic-workflows
"""

from ibm_watsonx_orchestrate.flow_builder.flows import (
    Flow, flow, START, END, Branch
)
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

# Define input schema
class MyWorkflowInput(BaseModel):
    """Input schema for the workflow."""
    param1: str = Field(description="Description of first parameter")
    param2: int = Field(description="Description of second parameter")
    param3: float = Field(description="Description of third parameter", default=0.0)

# Define output schema
class MyWorkflowOutput(BaseModel):
    """Output schema for the workflow."""
    status: str = Field(description="Processing status: success, failed, or pending")
    result: Dict[str, Any] = Field(description="Processing result data")
    message: str = Field(description="Human-readable message")

@flow(
    name="my_workflow_name",
    description="Clear description of what this workflow does and when to use it",
    input_schema=MyWorkflowInput,
    output_schema=MyWorkflowOutput
)
def build_my_workflow(aflow: Flow) -> Flow:
    """
    Build the workflow graph.
    
    This workflow performs the following steps:
    1. [Step 1 description]
    2. [Step 2 description]
    3. [Step 3 description]
    
    Args:
        aflow (Flow): The flow builder instance
        
    Returns:
        Flow: The configured workflow
        
    Note:
        watsonx Orchestrate automatically maps data at runtime based on parameter names.
        Tools receive data when their parameter names match the expression references.
    """
    
    # Step 1: Define tool nodes
    # CRITICAL: Use full toolkit:tool_name format
    step1_node = aflow.tool("toolkit-name:tool_name_1")
    
    # Step 2: Another tool node
    # Automatic mapping: If tool_name_2 has parameters matching step1_node output fields,
    # they will be automatically populated at runtime
    step2_node = aflow.tool("toolkit-name:tool_name_2")
    
    # Step 3: Create conditional branch
    # Evaluator expression references node outputs: "node_name.output.field_name"
    # The evaluator is a string expression that will be evaluated at runtime
    decision_branch: Branch = aflow.branch(
        evaluator="step2_node.output.score > 0.5"  # type: ignore[arg-type]
    )
    
    # Success path node
    success_node = aflow.tool("toolkit-name:success_handler")
    
    # Failure path node
    failure_node = aflow.tool("toolkit-name:failure_handler")
    
    # Build the graph
    # Connect START to first node
    aflow.edge(START, step1_node)
    
    # Connect nodes in sequence
    aflow.edge(step1_node, step2_node)
    
    # Connect to branch
    aflow.edge(step2_node, decision_branch)
    
    # Define branch cases
    decision_branch.case(True, success_node)
    decision_branch.case(False, failure_node)
    
    # Connect to END
    aflow.edge(success_node, END)
    aflow.edge(failure_node, END)
    
    return aflow


# Alternative pattern: Sequential workflow without branching
@flow(
    name="simple_workflow",
    description="Simple sequential workflow",
    input_schema=MyWorkflowInput,
    output_schema=MyWorkflowOutput
)
def build_simple_workflow(aflow: Flow) -> Flow:
    """
    Simple sequential workflow without branching.
    
    Demonstrates the sequence() helper for linear workflows.
    """
    
    # Define nodes
    node1 = aflow.tool("toolkit:tool1")
    node2 = aflow.tool("toolkit:tool2")
    node3 = aflow.tool("toolkit:tool3")
    
    # Build sequential graph using helper method
    # This is equivalent to: edge(START, node1), edge(node1, node2), etc.
    aflow.sequence(START, node1, node2, node3, END)
    
    return aflow


# Alternative pattern: Multiple branches
@flow(
    name="multi_branch_workflow",
    description="Workflow with multiple conditional branches",
    input_schema=MyWorkflowInput,
    output_schema=MyWorkflowOutput
)
def build_multi_branch_workflow(aflow: Flow) -> Flow:
    """
    Workflow demonstrating multiple conditional branches.
    
    Shows how to handle multiple decision points in a workflow.
    """
    
    # Define nodes
    check_node = aflow.tool("toolkit:check_condition")
    
    # Create branch with multiple conditions
    status_branch: Branch = aflow.branch(
        evaluator="check_node.output.status"  # type: ignore[arg-type]
    )
    
    # Define nodes for each status
    approved_node = aflow.tool("toolkit:handle_approved")
    rejected_node = aflow.tool("toolkit:handle_rejected")
    pending_node = aflow.tool("toolkit:handle_pending")
    
    # Build graph
    aflow.edge(START, check_node)
    aflow.edge(check_node, status_branch)
    
    # Define cases for different status values
    status_branch.case("approved", approved_node)
    status_branch.case("rejected", rejected_node)
    status_branch.case("pending", pending_node)
    
    # Connect all paths to END
    aflow.edge(approved_node, END)
    aflow.edge(rejected_node, END)
    aflow.edge(pending_node, END)
    
    return aflow


# Alternative pattern: Parallel execution with foreach
class ItemInput(BaseModel):
    """Schema for individual items to process."""
    item_id: str = Field(description="Item identifier")
    data: Dict[str, Any] = Field(description="Item data")

class ItemOutput(BaseModel):
    """Schema for processed item output."""
    item_id: str = Field(description="Item identifier")
    result: Dict[str, Any] = Field(description="Processing result")

class ParallelWorkflowInput(BaseModel):
    """Input schema for parallel workflow."""
    items: List[ItemInput] = Field(description="List of items to process")

@flow(
    name="parallel_workflow",
    description="Workflow with parallel item processing using foreach",
    input_schema=ParallelWorkflowInput,
    output_schema=MyWorkflowOutput
)
def build_parallel_workflow(aflow: Flow) -> Flow:
    """
    Workflow that processes items in parallel using foreach.
    
    The foreach construct processes each item in the input list independently,
    allowing for parallel execution.
    
    Note: The exact foreach API may vary. Consult official documentation for
    the current syntax. This example shows the conceptual pattern.
    """
    
    # Define the processing tool that will be applied to each item
    process_node = aflow.tool("toolkit:process_item")
    
    # Create foreach node for parallel execution
    # Note: Syntax may vary - check official docs for current API
    foreach_node = aflow.foreach(  # type: ignore[call-arg]
        items="flow.input.items",  # type: ignore[arg-type]  # Reference to input list
        body=process_node  # type: ignore[arg-type]  # Tool to apply to each item
    )
    
    # Aggregate results from all parallel executions
    aggregate_node = aflow.tool("toolkit:aggregate_results")
    
    # Build graph
    aflow.edge(START, foreach_node)
    aflow.edge(foreach_node, aggregate_node)
    aflow.edge(aggregate_node, END)
    
    return aflow


# Pattern: Complex workflow with multiple branches
@flow(
    name="complex_workflow",
    description="Complex workflow with multiple decision points",
    input_schema=MyWorkflowInput,
    output_schema=MyWorkflowOutput
)
def build_complex_workflow(aflow: Flow) -> Flow:
    """
    Complex workflow demonstrating multiple branches and paths.
    
    Shows how to handle multiple decision points in a single workflow.
    """
    
    # Initial validation
    validate_node = aflow.tool("toolkit:validate_input")
    
    # First decision point
    validation_branch: Branch = aflow.branch(
        evaluator="validate_node.output.is_valid"  # type: ignore[arg-type]
    )
    
    # Valid path - process normally
    process_node = aflow.tool("toolkit:process_data")
    
    # Second decision point based on processing result
    result_branch: Branch = aflow.branch(
        evaluator="process_node.output.confidence > 0.8"  # type: ignore[arg-type]
    )
    
    # High confidence - auto-approve
    auto_approve_node = aflow.tool("toolkit:auto_approve")
    
    # Low confidence - manual review
    manual_review_node = aflow.tool("toolkit:request_review")
    
    # Invalid path - reject immediately
    reject_node = aflow.tool("toolkit:reject_input")
    
    # Build graph
    aflow.edge(START, validate_node)
    aflow.edge(validate_node, validation_branch)
    
    # Valid path
    validation_branch.case(True, process_node)
    aflow.edge(process_node, result_branch)
    result_branch.case(True, auto_approve_node)
    result_branch.case(False, manual_review_node)
    aflow.edge(auto_approve_node, END)
    aflow.edge(manual_review_node, END)
    
    # Invalid path
    validation_branch.case(False, reject_node)
    aflow.edge(reject_node, END)
    
    return aflow


"""
IMPORT INSTRUCTIONS:
====================

1. Import workflow as a flow-type tool:
   orchestrate tools import -k flow -f tools/my_workflow.py

2. Verify import:
   orchestrate tools list | grep my_workflow_name

3. Use in agent YAML:
   tools:
     - my_workflow_name

4. Test through agent (workflows can only be tested via agents in non-local environments)

AUTOMATIC DATA MAPPING:
=======================

watsonx Orchestrate automatically maps data at runtime based on:
- Parameter names matching expression references
- Node output fields matching tool input parameters
- Flow input fields matching tool parameters

Example:
  If tool "check_credit" has parameter "customer_id" and the workflow input
  has field "customer_id", they are automatically connected at runtime.

Expression References:
- flow.input.field_name - Reference workflow input
- node_name.output.field_name - Reference previous node output

NO MANUAL MAPPING REQUIRED:
The platform handles all data flow automatically. The old map_input() method
is not part of the official API and should not be used.

WORKFLOW vs AGENT:
==================

Use Workflows When:
- Process is deterministic and follows fixed sequence
- Steps are well-defined with clear inputs/outputs
- Performance and cost optimization are critical (60% faster, 80% lower cost)
- No LLM reasoning needed between steps
- Examples: loan approval, order processing, data validation

Use Agents When:
- Process requires dynamic decision-making
- Steps depend on LLM reasoning and context
- Flexibility and adaptability are more important
- User interaction and conversation are needed
- Examples: customer support, complex problem-solving

BRANCHING PATTERNS:
===================

Simple Boolean Branch:
  branch = aflow.branch(evaluator="node.output.field > threshold")
  branch.case(True, success_node)
  branch.case(False, failure_node)

Multi-value Branch:
  branch = aflow.branch(evaluator="node.output.status")
  branch.case("approved", approved_node)
  branch.case("rejected", rejected_node)
  branch.case("pending", pending_node)

FOREACH PATTERN:
================

Note: The foreach API may evolve. Always consult the official documentation
for the current syntax and capabilities.

Basic pattern:
  foreach_node = aflow.foreach(
      items="flow.input.items",
      body=processing_tool
  )

The foreach construct applies the body tool to each item in the list,
enabling parallel processing of multiple items.
"""

# Made with Bob
