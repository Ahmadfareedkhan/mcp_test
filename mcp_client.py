from datetime import datetime
from mcp_server import process_mcp_message

def current_timestamp():
    """Return the current UTC timestamp in ISO format."""
    return datetime.utcnow().isoformat()

def format_query(user_query):
    """
    Format the user query into an MCP-compliant JSON message.
    """
    mcp_message = {
        "type": "query",
        "sender": "MCP_Client",
        "payload": {"query": user_query},
        "timestamp": current_timestamp()
    }
    return mcp_message

def send_query_to_server(mcp_message):
    """
    Simulate sending the MCP message to the server.
    In a production system, this could involve network communication.
    Here, we directly call the server function.
    """
    return process_mcp_message(mcp_message)

def display_result(response_message):
    """
    Display the server's response to the user.
    """
    if response_message.get("type") == "response":
        print("Execution Result:")
        print(response_message["payload"]["result"])
        print("Command executed:", response_message["payload"]["command"])
    elif response_message.get("type") == "error":
        print("An error occurred:")
        print(response_message["payload"]["error"])

def main():
    user_query = input("Enter your command query (e.g., 'list files', 'current directory', 'disk usage'): ")
    client_message = format_query(user_query)
    response = send_query_to_server(client_message)
    display_result(response)

if __name__ == "__main__":
    main()
