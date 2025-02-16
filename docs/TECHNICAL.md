# MCP Client-Server with LLM Command Execution

A Model Context Protocol (MCP) implementation that enables dynamic system command generation and execution through LLM integration.

## Overview

This project implements a client-server system using the Model Context Protocol (MCP) to enable:
- Natural language command generation using LLMs (Groq)
- Secure command execution with validation
- Standardized communication using MCP format
- Real-time system information querying

### Architecture

```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│   Client    │    │     LLM      │    │    Server    │
│ (MCP Client)│───▶│(Groq Service)│───▶│ (MCP Server) │
└─────────────┘    └──────────────┘    └──────────────┘
       ▲                                       │
       └───────────────────────────────────────┘
                   Results via MCP
```

## Features

- **MCP Client**
  - Natural language query processing
  - LLM integration for command generation
  - MCP-compliant communication
  - Error handling and logging

- **MCP Server**
  - Secure command execution
  - Resource management
  - Tool and prompt support
  - Formatted output handling

## Requirements

- Python 3.10 or higher
- Groq API key for LLM service
- Required Python packages:
  - mcp
  - groq
  - httpx
  - logging

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd [repository-name]
```

2. Install dependencies:
```bash
pip install mcp groq httpx
```

3. Set up environment variables:
```bash
# Create .env file
echo "GROQ_API_KEY=your_api_key_here" > .env
```

## File Structure

```
├── mcp_client.py    # MCP client implementation
├── mcp_server.py    # MCP server implementation
├── llm_utils.py     # LLM integration utilities
└── README.md        # Documentation
```

## Technical Implementation

### MCP Client

The client implementation:
- Uses the MCP Python SDK for protocol compliance
- Integrates with Groq for command generation
- Maintains proper MCP session management
- Handles tool execution and responses

Key components:
```python
class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.groq = Groq()
```

### MCP Server

The server implementation:
- Follows MCP protocol specification
- Provides tool and resource capabilities
- Implements secure command execution
- Handles output formatting

Key components:
```python
class MCPServer:
    def __init__(self, name: str = "CommandExecutionServer"):
        self.mcp = FastMCP(
            name=name,
            version="1.0.0"
        )
```

## Usage

1. Start the server:
```bash
python mcp_server.py
```

2. Run client queries:
```bash
python mcp_client.py "list the top CPU processes"
python mcp_client.py "show network adapter configuration"
```

## MCP Protocol Compliance

This implementation follows the official MCP specification for:

1. Protocol Initialization
   - Proper capability negotiation
   - Version compatibility checks
   - Session establishment

2. Message Format
   - Standard JSON-RPC message structure
   - Proper content typing
   - Error handling format

3. Tools and Resources
   - Tool registration and execution
   - Resource management
   - Prompt handling

## Security Considerations

The implementation includes several security measures:

1. Command Validation
   - Blocked dangerous commands
   - Input sanitization
   - Execution timeouts

2. Error Handling
   - Graceful error recovery
   - Proper error reporting
   - Resource cleanup

3. Logging
   - Operation logging
   - Error tracking
   - Audit trail

## Testing

You can test the system using:

1. Direct execution:
```bash
python mcp_client.py "your command here"
```

2. MCP Inspector:
```bash
npx @modelcontextprotocol/inspector
```

## References

- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- [MCP Specification](https://spec.modelcontextprotocol.io)
- [Protocol Architecture](https://modelcontextprotocol.io/docs/concepts/architecture)

