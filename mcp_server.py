import subprocess
import shlex
import logging
from typing import Optional

from mcp.server.fastmcp import FastMCP
from mcp.types import CallToolResult

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MCPServer:
    def __init__(self, name: str = "CommandExecutionServer", version: str = "1.0.0"):
        # Initialize server with proper capabilities
        self.mcp = FastMCP(
            name=name,
            version=version
        )
        self._setup_tools()
        self._setup_resources()
        self._setup_prompts()

    def _setup_tools(self):
        """Configure available tools"""
        @self.mcp.tool()
        def execute_command(command: str) -> CallToolResult:
            """
            Executes a shell command securely with validation.
            
            Args:
                command: The command string to execute
                
            Returns:
                CallToolResult containing command output or error message
            """
            logger.info(f"[Server] Requested to execute command: {command}")
            
            try:
                # Validate command
                tokens = shlex.split(command)
                for token in tokens:
                    if token in ["rm", "shutdown", "reboot", "mkfs", "dd"]:
                        error_msg = f"[SECURITY] The token '{token}' is disallowed."
                        logger.warning(error_msg)
                        return CallToolResult(
                            content=[{
                                "type": "text",
                                "text": error_msg
                            }],
                            is_error=True
                        )

                # Execute command
                proc = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                # Prepare output according to MCP standard format
                output = proc.stdout + "\n" + proc.stderr
                if proc.returncode != 0:
                    output += f"\n[Command exited with code: {proc.returncode}]"
                
                logger.info(f"[Server] Execution completed. Return code={proc.returncode}")
                
                return CallToolResult(
                    content=[{
                        "type": "text",
                        "text": output.strip()
                    }]
                )

            except subprocess.TimeoutExpired:
                error_msg = "[ERROR] Command execution timed out after 30 seconds"
                logger.error(error_msg)
                return CallToolResult(
                    content=[{
                        "type": "text",
                        "text": error_msg
                    }],
                    is_error=True
                )
            except Exception as e:
                error_msg = f"[ERROR] {str(e)}"
                logger.exception("Error executing command:")
                return CallToolResult(
                    content=[{
                        "type": "text",
                        "text": error_msg
                    }],
                    is_error=True
                )

    def _setup_resources(self):
        """Configure available resources"""
        @self.mcp.resource("system://processes")
        def get_processes() -> str:
            """Get the list of running processes"""
            cmd = 'powershell /c "Get-Process | Sort-Object CPU -Descending | Select-Object -First 10"'
            proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return proc.stdout

    def _setup_prompts(self):
        """Configure available prompts"""
        @self.mcp.prompt()
        def system_query(query: str) -> str:
            """Query system information"""
            return f"Please analyze this system information: {query}"

    def run(self):
        """Start the MCP server with proper initialization"""
        logger.info(f"Starting {self.mcp.name}  on stdio ...")
        try:
            self.mcp.run()
        except Exception as e:
            logger.error(f"Server error: {e}")
            raise
        finally:
            logger.info("MCP server shut down.")

if __name__ == "__main__":
    server = MCPServer()
    server.run()