from common import current_timestamp, log_interaction, validate_command, generate_command_from_query, execute_system_command

def process_mcp_message(mcp_message):
    """
    Process an incoming MCP message:
      - Extracts the user query.
      - Uses the simulated LLM to generate a system command.
      - Validates and executes the command.
      - Returns an MCP-compliant response message.
    """
    try:
        query = mcp_message.get("payload", {}).get("query", "")
        if not query:
            raise ValueError("Empty query received.")
        
        # Generate command using simulated LLM logic
        command = generate_command_from_query(query)
        # Validate the command to prevent dangerous operations
        validate_command(command)
        # Execute the command securely
        execution_result = execute_system_command(command)
        
        response_message = {
            "type": "response",
            "sender": "MCP_Server",
            "payload": {"result": execution_result, "command": command},
            "timestamp": current_timestamp()
        }
    except Exception as error:
        response_message = {
            "type": "error",
            "sender": "MCP_Server",
            "payload": {"error": str(error)},
            "timestamp": current_timestamp()
        }
    # Log the interaction for auditing and debugging
    log_interaction(mcp_message, response_message)
    return response_message

# Standalone test for the MCP server:
if __name__ == "__main__":
    test_message = {
        "type": "query",
        "sender": "MCP_Client",
        "payload": {"query": "list files"},
        "timestamp": current_timestamp()
    }
    response = process_mcp_message(test_message)
    print("Test Response:", response)
