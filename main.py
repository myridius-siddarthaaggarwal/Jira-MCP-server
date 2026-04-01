import os
from mcp.server.fastmcp import FastMCP
from tools.jira_tools import register_tools

# Initialize FastMCP Server
mcp = FastMCP("jira-mcp-server")

# Register all Jira tools
register_tools(mcp)

if __name__ == "__main__":
    # This runs the MCP server via standard input/output (for Claude Desktop)
    mcp.run()
