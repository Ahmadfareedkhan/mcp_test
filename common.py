import json
import logging
from datetime import datetime
import subprocess

# Setup logging to file "mcp_system.log"
logging.basicConfig(
    filename='mcp_system.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

def current_timestamp():
    """Return the current UTC timestamp in ISO format."""
    return datetime.utcnow().isoformat()

def log_interaction(request, response):
    """Log both the incoming MCP request and the response in JSON format."""
    logging.info("Request: %s", json.dumps(request))
    logging.info("Response: %s", json.dumps(response))

def validate_command(command):
    """
    Validate that the generated command does not include dangerous operations.
    Raises ValueError if a forbidden keyword is found.
    """
    forbidden_keywords = ["rm -rf", "shutdown", "mkfs", "dd if="]
    for keyword in forbidden_keywords:
        if keyword in command:
            raise ValueError(f"Unsafe command detected: {command}")
    return True

def execute_system_command(command):
    """
    Execute the validated system command securely using subprocess.
    Returns the output or an error message.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Command execution failed: {e.stderr.strip()}"
    except Exception as e:
        return f"Error during command execution: {str(e)}"
