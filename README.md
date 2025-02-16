# MCP Command Execution System

A Model Context Protocol (MCP) implementation that enables natural language system commands through LLM integration.

## Quick Start

1. **Install Dependencies**
```bash
pip install mcp groq httpx python-dotenv
```

2. **Set Up Environment**
```bash
# Create .env file with your Groq API key
echo "GROQ_API_KEY=your_api_key_here" > .env
```

3. **Run the System**
```bash
# Start the server in one terminal
python mcp_server.py

# Run commands in another terminal
python mcp_client.py "list the top CPU processes"
python mcp_client.py "show network adapter configuration"
```

## Features

- Natural language to system command translation
- Secure command execution with validation
- Real-time system information querying
- Formatted output display

## Components

### MCP Client
- Processes natural language queries
- Integrates with Groq LLM
- Handles MCP protocol communication
- Manages command execution

### MCP Server
- Executes system commands securely
- Provides resource access
- Formats command output
- Implements MCP protocol standards

## Usage Examples

```bash
# System processes
python mcp_client.py "show me the processes using the most memory"

# Network configuration
python mcp_client.py "display network adapter status"

# System information
python mcp_client.py "show CPU information"
```

## Requirements

- Python 3.10 or higher
- Groq API key
- Windows PowerShell (for system commands)

## Project Structure

```
├── mcp_client.py    # Client implementation
├── mcp_server.py    # Server implementation
├── llm_utils.py     # LLM integration
└── .env            # Environment variables
```

## Technical Details

For detailed technical information about the implementation, including:
- Architecture diagrams
- Protocol compliance
- Security considerations
- Testing procedures

Please refer to the [Technical Documentation](docs/TECHNICAL.md).

## References

- [Model Context Protocol](https://modelcontextprotocol.io)
- [MCP Specification](https://spec.modelcontextprotocol.io)
- [Groq API Documentation](https://docs.groq.com)

## Security Notes

- The server implements command validation
- Dangerous system commands are blocked
- All operations are logged
- Execution timeouts are enforced

## Contributing

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details.