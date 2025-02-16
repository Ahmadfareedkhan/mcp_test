import asyncio
import sys
import logging

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from llm_utils import generate_command_with_ollama

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def main():
    if len(sys.argv) < 2:
        print("Usage: python mcp_client.py \"<Your question here>\"")
        sys.exit(1)

    user_query = sys.argv[1]
    logger.info(f"[Client] User query: {user_query}")

    # 1) Use the local LLM (Ollama) to generate a shell command
    generated_cmd = generate_command_with_ollama(user_query)
    logger.info(f"[Client] LLM suggested command: {generated_cmd}")

    # 2) Connect to the MCP server (which should be run in a separate terminal)
    #    Alternatively, we can let the client spawn the server by specifying
    #    the 'command' + 'args' for the local process.
    #    For example, to automatically spawn the server:
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"]
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            # Now we can call the 'execute_command' tool on the server
            logger.info("[Client] Calling 'execute_command' on the server ...")
            tool_result = await session.call_tool(
                "execute_command",
                {"command": generated_cmd}
            )

            # The 'tool_result' is of type ToolResult, with a 'content' list
            if not tool_result.content:
                print("[Client] No content returned from server.")
                return
            # Typically we have a list of content items, each might be text
            result_text = tool_result.content[0].text
            logger.info("[Client] Received server result:\n" + result_text)
            print("\n=== MCP Server Execution Result ===")
            print(result_text)

if __name__ == "__main__":
    asyncio.run(main())
