"""
LangGraph Agent Template

This template provides a basic structure for creating a LangGraph agent
for watsonx Orchestrate.

CRITICAL: The factory function must return an UNCOMPILED StateGraph.
The platform compiles the graph at runtime.
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional, List, Any


class AgentState(TypedDict):
    """
    Define the state structure for your agent.
    
    Add fields that represent the data your agent needs to track
    throughout its execution.
    """
    # Example fields - customize for your use case
    user_input: str
    context: Optional[str]
    results: List[Any]
    final_output: str


def create_agent() -> StateGraph:
    """
    Factory function that creates the agent graph.
    
    This function is called by watsonx Orchestrate to instantiate your agent.
    The entrypoint in agent.yaml should point to this function.
    
    CRITICAL: Return the StateGraph UNCOMPILED.
    Do NOT call .compile() - the platform handles compilation.
    
    Returns:
        StateGraph: Uncompiled StateGraph instance
    """
    # Create the graph with your state definition
    graph = StateGraph(AgentState)
    
    # Add nodes (processing steps)
    graph.add_node("process_input", process_input_node)
    graph.add_node("execute_task", execute_task_node)
    graph.add_node("generate_output", generate_output_node)
    
    # Define the flow
    graph.set_entry_point("process_input")
    graph.add_edge("process_input", "execute_task")
    graph.add_edge("execute_task", "generate_output")
    graph.add_edge("generate_output", END)
    
    # Return uncompiled graph
    return graph


def process_input_node(state: AgentState) -> AgentState:
    """
    Process and validate user input.
    
    Args:
        state: Current agent state
        
    Returns:
        AgentState: Updated state with processed input
    """
    user_input = state.get("user_input", "")
    
    # Process the input
    # Example: Extract key information, validate format, etc.
    processed_context = f"Processing: {user_input}"
    
    # Update state
    state["context"] = processed_context
    return state


def execute_task_node(state: AgentState) -> AgentState:
    """
    Execute the main task logic.
    
    Args:
        state: Current agent state
        
    Returns:
        AgentState: Updated state with task results
    """
    context = state.get("context", "")
    
    # Execute your main logic here
    # Example: Call external APIs, process data, etc.
    results = [
        {"item": "result1", "value": "data1"},
        {"item": "result2", "value": "data2"}
    ]
    
    # Update state
    state["results"] = results
    return state


def generate_output_node(state: AgentState) -> AgentState:
    """
    Generate the final output.
    
    Args:
        state: Current agent state
        
    Returns:
        AgentState: Updated state with final output
    """
    results = state.get("results", [])
    
    # Generate final output
    # Example: Format results, create summary, etc.
    output = f"Completed processing with {len(results)} results"
    
    # Update state
    state["final_output"] = output
    return state


# Optional: Add conditional routing example
def should_retry(state: AgentState) -> str:
    """
    Example conditional routing function.
    
    Args:
        state: Current agent state
        
    Returns:
        str: Next node name based on condition
    """
    results = state.get("results", [])
    
    if len(results) == 0:
        return "retry"
    else:
        return "continue"


# Optional: Example with conditional edges
def create_agent_with_conditionals() -> StateGraph:
    """
    Example factory function with conditional routing.
    
    Returns:
        StateGraph: Uncompiled StateGraph with conditional logic
    """
    graph = StateGraph(AgentState)
    
    # Add nodes
    graph.add_node("process_input", process_input_node)
    graph.add_node("execute_task", execute_task_node)
    graph.add_node("retry", process_input_node)  # Retry uses same logic
    graph.add_node("generate_output", generate_output_node)
    
    # Define flow with conditional routing
    graph.set_entry_point("process_input")
    graph.add_edge("process_input", "execute_task")
    
    # Conditional edge based on results
    graph.add_conditional_edges(
        "execute_task",
        should_retry,
        {
            "retry": "retry",
            "continue": "generate_output"
        }
    )
    
    graph.add_edge("retry", "execute_task")
    graph.add_edge("generate_output", END)
    
    return graph


# Optional: Example with external LLM integration
def create_agent_with_llm() -> StateGraph:
    """
    Example factory function with external LLM integration.
    
    Requires:
    - Connection configured in watsonx Orchestrate
    - API key stored in connection
    
    Returns:
        StateGraph: Uncompiled StateGraph with LLM integration
    """
    from langchain_openai import ChatOpenAI
    from ibm_watsonx_orchestrate import get_connection
    
    # Get API credentials from connection
    # Connection must be created before importing agent
    openai_key = get_connection("openai")["api_key"]
    llm = ChatOpenAI(api_key=openai_key, model="gpt-4")
    
    graph = StateGraph(AgentState)
    
    # Add nodes with LLM access
    graph.add_node("process", lambda state: process_with_llm(state, llm))
    graph.add_node("generate", lambda state: generate_with_llm(state, llm))
    
    graph.set_entry_point("process")
    graph.add_edge("process", "generate")
    graph.add_edge("generate", END)
    
    return graph


def process_with_llm(state: AgentState, llm) -> AgentState:
    """Example node using LLM"""
    user_input = state.get("user_input", "")
    response = llm.invoke(f"Process this input: {user_input}")
    state["context"] = response.content
    return state


def generate_with_llm(state: AgentState, llm) -> AgentState:
    """Example node using LLM for generation"""
    context = state.get("context", "")
    response = llm.invoke(f"Generate output for: {context}")
    state["final_output"] = response.content
    return state

# Made with Bob
