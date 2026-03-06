import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

from dotenv import load_dotenv
load_dotenv()

# --- MCP Tools ---
# Model Context Protocol (MCP) is an open standard for connecting AI agents to external tools.
# ADK's McpToolset connects to any MCP server and auto-discovers its tools.
# Here we use the filesystem MCP server to give the agent safe, read-only file access.

# Define the directory the agent is allowed to access
_allowed_path = os.path.dirname(os.path.abspath(__file__))

root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="file_assistant",
    description="An agent that can read and explore files using MCP filesystem tools.",
    instruction=f"""You are a helpful file assistant.
    You have access to the filesystem through MCP tools.
    The allowed directory is: {_allowed_path}
    You can read files, list directories, and search for files.
    Always respect the allowed directory boundaries.
    When showing file contents, format them nicely for the user.""",
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx",
                    args=[
                        "-y",
                        "@modelcontextprotocol/server-filesystem",
                        _allowed_path,
                    ],
                ),
                timeout=10,
            ),
            # Filter tools for security — only allow read operations
            tool_filter=[
                "read_file",
                "read_multiple_files",
                "list_directory",
                "directory_tree",
                "search_files",
                "get_file_info",
                "list_allowed_directories",
            ],
        )
    ],
)

# NOTE: This agent is designed to be run with `adk run` or `adk web`.
# The MCP toolset requires async initialization, which the ADK CLI handles automatically.
#
# To run (from the Lab-7 directory):
#   adk run file_assistant
#   OR
#   adk web file_assistant
#
# Then try queries like:
#   "List the files in the current directory"
#   "Read the contents of requirements.txt"
#   "Show me the directory tree"
