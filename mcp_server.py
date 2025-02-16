import subprocess
import shlex
import logging

import mcp.types as types
from mcp.server.fastmcp import FastMCP

# Create a logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)  # or DEBUG, etc.

# Create the MCP server instance
mcp = FastMCP("LLMCommandExecutionServer")

DISALLOWED_TOKENS = ["rm", "shutdown", "reboot", "mkfs", "dd"]

@mcp.tool()
def execute_command(command: str) -> str:
    """
    Executes a shell command and returns stdout + stderr.
    We do minimal checks so we don't run obviously harmful commands.

    Returns a text containing either the command output or
    an error message if blocked or if an error occurs.
    """
    logger.info(f"[Server] Requested to execute command: {command}")

    # Very basic "security" measure: check tokens
    tokens = shlex.split(command)
    for t in tokens:
        if t in DISALLOWED_TOKENS:
            logger.warning(f"Blocked token '{t}' in command.")
            return f"[SECURITY BLOCKED] The token '{t}' is disallowed."

    try:
        proc = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = proc.stdout + "\n" + proc.stderr
        code = proc.returncode
        if code != 0:
            output += f"\n[Command exited with non-zero code: {code}]"
        logger.info(f"[Server] Execution completed. Return code={code}")
        return output.strip()
    except Exception as e:
        logger.exception("Error executing command:")
        return f"[ERROR] {e}"

if __name__ == "__main__":
    # Start the server on stdio
    logger.info("Starting MCP server on stdio ...")
    mcp.run()
    logger.info("MCP server shut down.")
