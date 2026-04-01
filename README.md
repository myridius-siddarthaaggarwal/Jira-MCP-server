# Jira MCP Server

A Model Context Protocol (MCP) server that connects **Claude Desktop** to Jira, enabling it to create tickets, fetch issue details, add comments, and more — all through natural language.

---

## Prerequisites

Install the following before getting started:

| Tool | Download |
|---|---|
| **Python 3.10+** | https://www.python.org/downloads/ |
| **Git** | https://git-scm.com/downloads |
| **VS Code** *(recommended editor)* | https://code.visualstudio.com/ |
| **Claude Desktop** | https://claude.ai/download |

> After installing Python, verify it works: `python --version`  
> After installing Git, verify it works: `git --version`

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/myridius-siddarthaaggarwal/Jira-MCP-server.git
cd Jira-MCP-server
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:
- **Windows:** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Connecting to Claude Desktop

This server runs automatically inside **Claude Desktop** via the MCP protocol. Follow these steps to register it:

### Step 1 — Find the Claude Desktop config file

Open this file in any text editor (VS Code recommended):

- **Windows:** `C:\Users\<YourUsername>\AppData\Roaming\Claude\claude_desktop_config.json`
- **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`

> If the file doesn't exist, create it.

### Step 2 — Add the Jira MCP server entry

Add the following inside the `mcpServers` block. Replace the path and credentials with your own:

```json
{
  "mcpServers": {
    "jira-mcp-server": {
      "command": "C:\\Users\\<YourUsername>\\Jira-MCP-server\\start_mcp.bat",
      "env": {
        "JIRA_BASE_URL": "https://yourorg.atlassian.net",
        "JIRA_EMAIL": "you@example.com",
        "JIRA_API_TOKEN": "your_api_token_here"
      }
    }
  }
}
```

> ⚠️ Replace `<YourUsername>` with your actual Windows username  
> ⚠️ Replace the path if you cloned the repo to a different folder

### Step 3 — Get your Jira API Token

1. Go to: https://id.atlassian.com/manage-profile/security/api-tokens
2. Click **Create API token**
3. Copy the token and paste it into `JIRA_API_TOKEN` above

### Step 4 — Restart Claude Desktop

Close and reopen Claude Desktop. The Jira tools will now be available automatically — you'll see a 🔨 tools icon in the chat interface.

---

## How `start_mcp.bat` works

When Claude Desktop launches this server, it runs `start_mcp.bat` which:
1. Activates the local Python virtual environment (`venv`)
2. Starts `main.py` — the MCP server

This means you **do not** need to manually start the server. Claude handles it automatically.

---

## Available Tools (usable in Claude)

Once connected, you can ask Claude things like:

- *"Create a bug ticket in project XYZ for login page crash"*
- *"Fetch details of ticket PROJ-123"*
- *"Add a comment to PROJ-456 saying it's been fixed"*
- *"List all projects in Jira"*

Internally these map to:

| Tool | Description |
|---|---|
| **Create Bug** | Creates a Jira bug report |
| **Get Issue** | Fetches details of a ticket by number |
| **Update Issue** | Updates fields of an existing issue |
| **Add Comment** | Adds a comment to an issue |
| **List Projects** | Lists all accessible Jira projects |
| **List Issues** | Lists issues in a project |

---

## Project Structure

```
Jira-MCP-Server/
├── main.py              # MCP server entry point
├── start_mcp.bat        # Launcher used by Claude Desktop (Windows)
├── requirements.txt     # Python dependencies
├── .gitignore           # Excludes venv, secrets, cache
├── api/
│   └── jira_client.py   # Jira REST API client
├── config/
│   └── settings.py      # Reads credentials from environment variables
├── tools/
│   └── jira_tools.py    # MCP tool definitions
└── test_jira.py         # Basic tests
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Claude doesn't show Jira tools | Check the config file path and restart Claude Desktop |
| `python` not found | Make sure Python is added to PATH during installation |
| Authentication error | Verify `JIRA_BASE_URL`, `JIRA_EMAIL`, and `JIRA_API_TOKEN` are correct |
| `venv` activation fails | Re-run `python -m venv venv` inside the project folder |
