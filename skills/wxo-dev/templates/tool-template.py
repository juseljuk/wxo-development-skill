# Python Tool Template
# Copy this template and customize for your tool

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from typing import Dict, Any

@tool
def my_tool_name(param1: str, param2: int) -> Dict[str, Any]:
    """
    Brief description of what this tool does.
    
    Detailed explanation of the tool's purpose and behavior.
    Include any important notes or limitations.
    
    Args:
        param1 (str): Description of first parameter
        param2 (int): Description of second parameter
        
    Returns:
        Dict[str, Any]: Description of return value structure
            - status: "success" or "error"
            - data: Result data (when successful)
            - message: Error message (when error)
    
    Example:
        >>> my_tool_name("test", 42)
        {"status": "success", "data": {"result": "processed"}}
    """
    try:
        # Input validation
        if not param1 or len(param1.strip()) == 0:
            return {
                "status": "error",
                "message": "param1 cannot be empty"
            }
        
        if param2 < 0:
            return {
                "status": "error",
                "message": "param2 must be non-negative"
            }
        
        # Tool logic here
        result = process_data(param1, param2)
        
        # Return success response
        return {
            "status": "success",
            "data": {
                "result": result,
                "param1": param1,
                "param2": param2
            }
        }
        
    except ValueError as e:
        return {
            "status": "error",
            "message": f"Invalid input: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
        }


def process_data(param1: str, param2: int) -> Any:
    """
    Helper function for tool logic.
    Keep business logic separate from tool wrapper.
    """
    # Implement your logic here
    return f"Processed {param1} with {param2}"


# For testing: Create a test file without @tool decorator
# See examples.md for testing patterns

# Made with Bob
