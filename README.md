# Jira MCP Server

A Model Context Protocol (MCP) server that connects Claude (or any MCP-compatible AI) to Jira, enabling it to create tickets, fetch issue details, add comments, and more — all through natural language.

---

## Prerequisites

- Python 3.10+
- A Jira account with API access
- Claude Desktop (or any MCP-compatible client)

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/myridius-siddarthaaggarwal/Jira-MCP-server.git
cd Jira-MCP-server
```

### 2. Create a virtual environment (recommended)

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

## Configuration

Set the following environment variables before running the server:

| Variable | Description |
|---|---|
| `JIRA_BASE_URL` | Your Jira instance URL (e.g. `https://yourorg.atlassian.net`) |
| `JIRA_EMAIL` | Your Jira account email |
| `JIRA_API_TOKEN` | Your Jira API token ([generate one here](https://id.atlassian.com/manage-profile/security/api-tokens)) |
| `JIRA_OBSERVED_IN_FIELD_ID` | *(Optional)* Custom field ID, defaults to `customfield_10097` |

### Setting environment variables

**Windows (PowerShell):**
```powershell
$env:JIRA_BASE_URL="https://yourorg.atlassian.net"
$env:JIRA_EMAIL="you@example.com"
$env:JIRA_API_TOKEN="your_api_token_here"
```

**Mac/Linux:**
```bash
export JIRA_BASE_URL="https://yourorg.atlassian.net"
export JIRA_EMAIL="you@example.com"
export JIRA_API_TOKEN="your_api_token_here"
```

---

## Running the Server

```bash
python main.py
```

---

## Available Tools

- **Create Bug** — Creates a Jira bug report with summary, description, priority, and observed-in version
- **Get Issue** — Fetches details of a Jira issue by ticket number
- **Update Issue** — Updates fields of an existing Jira issue
- **Add Comment** — Adds a comment to a Jira issue
- **List Projects** — Lists all accessible Jira projects
- **List Issues** — Lists issues in a project with optional filters

---

## Project Structure

```
Jira-MCP-Server/
├── main.py              # MCP server entry point
├── requirements.txt     # Python dependencies
├── api/
│   └── jira_client.py   # Jira REST API client
├── config/
│   └── settings.py      # Credential loading from env vars
├── tools/
│   └── jira_tools.py    # MCP tool definitions
└── test_jira.py         # Basic tests
```
