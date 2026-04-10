# Jira MCP Server

A **Model Context Protocol (MCP)** server that connects [Claude Desktop](https://claude.ai/download) (or any MCP-compatible AI client) to **Jira Cloud**, enabling full project management through natural language — create issues, manage sprints, log time, link issues, update comments, and more.

**31 tools** covering the complete Jira workflow: issue creation & editing, sprint lifecycle, comment management, worklog tracking, issue linking, and team/project discovery.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Connecting to Claude Desktop](#connecting-to-claude-desktop)
- [Environment Variables](#environment-variables)
- [Available Tools](#available-tools)
- [Example Prompts](#example-prompts)
- [Project Structure](#project-structure)
- [Jira Setup Notes](#jira-setup-notes)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

| Tool | Version | Download |
|---|---|---|
| **Python** | 3.10+ | https://www.python.org/downloads/ |
| **Git** | Any | https://git-scm.com/downloads |
| **Claude Desktop** | Latest | https://claude.ai/download |
| **Jira Cloud** account | — | https://www.atlassian.com/software/jira |

Verify installations:

```bash
python --version   # Should print 3.10 or higher
git --version
```

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

| Platform | Command |
|---|---|
| **Windows** | `venv\Scripts\activate` |
| **Mac / Linux** | `source venv/bin/activate` |

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Connecting to Claude Desktop

The server is launched automatically by Claude Desktop — you do not need to start it manually.

### Step 1 — Locate the Claude Desktop config file

| Platform | Path |
|---|---|
| **Windows** | `C:\Users\<YourUsername>\AppData\Roaming\Claude\claude_desktop_config.json` |
| **Mac** | `~/Library/Application Support/Claude/claude_desktop_config.json` |

Create the file if it does not exist.

### Step 2 — Register the server

Paste the following into the config file, replacing the placeholder values:

**Windows:**
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

**Mac / Linux:**
```json
{
  "mcpServers": {
    "jira-mcp-server": {
      "command": "/bin/bash",
      "args": ["-c", "cd /path/to/Jira-MCP-server && source venv/bin/activate && python main.py"],
      "env": {
        "JIRA_BASE_URL": "https://yourorg.atlassian.net",
        "JIRA_EMAIL": "you@example.com",
        "JIRA_API_TOKEN": "your_api_token_here"
      }
    }
  }
}
```

> Replace `<YourUsername>` and paths with your actual values.

### Step 3 — Get a Jira API Token

1. Go to: https://id.atlassian.com/manage-profile/security/api-tokens
2. Click **Create API token**
3. Give it a name (e.g., `claude-mcp`) and copy the token
4. Paste it as the value of `JIRA_API_TOKEN` in the config above

### Step 4 — Restart Claude Desktop

Close and reopen Claude Desktop. The Jira tools will be available — look for the **🔨 tools icon** in the chat input area.

---

## Environment Variables

### Required

| Variable | Description | Example |
|---|---|---|
| `JIRA_BASE_URL` | Your Jira Cloud base URL | `https://yourorg.atlassian.net` |
| `JIRA_EMAIL` | Email address associated with your Atlassian account | `you@example.com` |
| `JIRA_API_TOKEN` | Jira API token (not your password) | `ATATxxxxxxxx` |

### Optional — Custom Field IDs

Jira uses custom field IDs that may differ between instances. The defaults below work for most Jira Cloud setups. Override them only if your instance uses different field IDs (check via Jira's field configuration or browser dev tools).

| Variable | Default | Field |
|---|---|---|
| `JIRA_SPRINT_FIELD_ID` | `customfield_10020` | Sprint |
| `JIRA_STORY_POINTS_FIELD_ID` | `customfield_10016` | Story Points |
| `JIRA_EPIC_LINK_FIELD_ID` | `customfield_10014` | Epic Link (Classic Jira) — set to `parent` for Next-gen projects |
| `JIRA_OBSERVED_IN_FIELD_ID` | `customfield_10097` | Observed In (Bug field, if your project uses it) |

**Next-gen / team-managed projects:** Set `JIRA_EPIC_LINK_FIELD_ID=parent` to link issues to epics using the parent relationship instead of the classic epic link field.

---

## Available Tools

### Issue Creation

| Tool | Description |
|---|---|
| `create_jira_bug` | Create a Bug with optional sprint, priority, labels, story points, epic link |
| `create_jira_story` | Create a Story with the same optional fields |
| `create_jira_task` | Create a Task with the same optional fields |
| `create_jira_epic` | Create an Epic with sprint, priority, labels, story points |

All creation tools accept these parameters:

| Parameter | Type | Description |
|---|---|---|
| `project_key` | string | Uppercase project key, e.g. `PROJ` |
| `summary` | string | Title of the issue |
| `description` | string | Detailed description |
| `assignee_account_id` | string | Atlassian Account ID of assignee (use `search_users` to find) |
| `sprint_id` | int | Numeric sprint ID (use `get_sprints` to find) |
| `priority` | string | `Highest`, `High`, `Medium`, `Low`, or `Lowest` |
| `labels` | list | List of label strings, e.g. `["backend", "regression"]` |
| `story_points` | float | Story point estimate, e.g. `5.0` |
| `epic_key` | string | Key of the parent epic, e.g. `PROJ-10` *(not for `create_jira_epic`)* |
| `observed_in` | string | Bug only — environment/version where the bug was seen |

---

### Issue Reading & Searching

| Tool | Description |
|---|---|
| `get_issue` | Fetch the raw Jira API response for an issue (full detail) |
| `fetch_ticket` | Fetch a human-readable summary: status, assignee, priority, sprint, story points, labels, epic, description |
| `search_issues` | Search using JQL (Jira Query Language) |
| `find_tickets` | Search by assignee, status, and/or keyword without writing JQL |

**`search_issues` JQL examples:**
```
project = PROJ AND status = "In Progress"
assignee = currentUser() AND sprint in openSprints()
project = PROJ AND issuetype = Bug AND priority = High
text ~ "login crash" ORDER BY created DESC
```

---

### Issue Editing

| Tool | Parameters | Description |
|---|---|---|
| `update_issue` | `issue_key`, + any field below | Update any combination of fields on any issue type |
| `assign_issue` | `issue_key`, `assignee_account_id` | Quick-assign or unassign (pass `""` to unassign) |

**`update_issue` editable fields:**

| Parameter | Description |
|---|---|
| `summary` | New title |
| `description` | New description |
| `assignee_account_id` | New assignee (pass `""` to unassign) |
| `priority` | New priority name |
| `labels` | Replaces all existing labels with new list |
| `story_points` | New story point value |
| `sprint_id` | Move to a different sprint |
| `epic_key` | Link to / change parent epic |
| `status_name` | Transition to a new status by name (e.g., `"In Progress"`, `"Done"`) |

---

### Status Transitions

| Tool | Description |
|---|---|
| `get_issue_transitions` | List all available transitions for an issue (returns names and IDs) |
| `transition_issue` | Apply a transition by numeric ID |

> **Tip:** Use `update_issue` with `status_name` to transition by name — no need to look up IDs first.

---

### Comment Management

| Tool | Description |
|---|---|
| `add_comment` | Add a new comment to an issue |
| `get_comments` | List all comments with ID, author, timestamp, and body text |
| `update_comment` | Edit the text of an existing comment by its ID |
| `delete_comment` | Delete a comment by its ID (irreversible) |

---

### Worklog / Time Tracking

| Tool | Description |
|---|---|
| `get_worklogs` | List all time logs on an issue (author, time spent, started) |
| `add_worklog` | Log time spent on an issue |

**`add_worklog` time formats:** `2h`, `1d`, `30m`, `1d 4h 30m`

---

### Sprint Management

| Tool | Description |
|---|---|
| `get_boards` | List all Agile boards (optionally filter by project key) |
| `get_sprints` | List sprints for a board — filter by `active`, `future`, or `closed` |
| `get_active_sprint` | Get the single active sprint for a board |
| `create_sprint` | Create a new sprint with optional name, goal, start/end dates |
| `update_sprint` | Rename, set goal, change dates, or change state (`active` to start, `closed` to complete) |
| `add_issues_to_sprint` | Move one or more issues into a sprint |
| `remove_issues_from_sprint` | Move one or more issues back to the backlog |

**Sprint workflow:**
1. `get_boards` → find your board ID
2. `create_sprint` → create a future sprint
3. `add_issues_to_sprint` → populate it
4. `update_sprint` with `state="active"` → start it
5. `update_sprint` with `state="closed"` → complete it

---

### Issue Linking

| Tool | Description |
|---|---|
| `get_issue_link_types` | List all available link types (`Blocks`, `Clones`, `Duplicate`, `Relates to`, etc.) |
| `link_issues` | Create a directional link between two issues |

---

### Discovery & Metadata

| Tool | Description |
|---|---|
| `get_project_info` | Project metadata — name, lead, type, available issue types, components |
| `get_issue_types` | List issue types available in a project |
| `get_priorities` | List all priority levels configured in Jira |
| `search_users` | Search users by name or email — returns account IDs for use in assignee fields |

---

## Example Prompts

Once connected to Claude Desktop, you can use natural language:

**Creating issues:**
- *"Create a high priority bug in project PROJ for the login page crash, assign it to john@example.com, add it to the current sprint, and give it 3 story points"*
- *"Create a story in PROJ called 'Redesign checkout flow' with 8 story points, link it to epic PROJ-10"*
- *"Create Sprint 5 on board 42 starting April 14th, ending April 28th, with goal 'Ship payments v2'"*

**Viewing & searching:**
- *"Fetch details of PROJ-123"*
- *"Show me all In Progress bugs assigned to me in project PROJ"*
- *"Search for tickets about payment failures in PROJ"*
- *"List all sprints for board 42"*

**Editing:**
- *"Move PROJ-123 to Done"*
- *"Change the priority of PROJ-456 to High and assign it to Sarah"*
- *"Update the story points on PROJ-789 to 5"*
- *"Add PROJ-100 and PROJ-101 to sprint 55"*
- *"Move PROJ-200 back to the backlog"*

**Comments & time:**
- *"Add a comment to PROJ-123 saying the fix has been deployed to staging"*
- *"Show all comments on PROJ-456"*
- *"Edit comment 12345 on PROJ-123 to say 'Fixed in v2.1'"*
- *"Log 2 hours of work on PROJ-789"*

**Linking & discovery:**
- *"Link PROJ-1 as blocking PROJ-2"*
- *"Find the account ID for john@example.com"*
- *"What issue types are available in project PROJ?"*
- *"List all priority levels in Jira"*

---

## Project Structure

```
Jira-MCP-Server/
├── main.py                # MCP server entry point — initialises FastMCP and registers tools
├── start_mcp.bat          # Windows launcher used by Claude Desktop
├── requirements.txt       # Python dependencies (mcp[cli], requests)
├── .gitignore             # Excludes venv, credentials, cache files
├── test_jira.py           # Manual integration test script
│
├── api/
│   └── jira_client.py     # All Jira REST API calls (api/3 and agile/1.0)
│
├── config/
│   └── settings.py        # Reads credentials and field IDs from environment variables
│
└── tools/
    └── jira_tools.py      # 31 MCP tool definitions registered with FastMCP
```

### How it works

```
Claude Desktop
     │
     │  MCP protocol (stdio)
     ▼
  main.py  ──registers──▶  tools/jira_tools.py  ──calls──▶  api/jira_client.py
                                                                     │
                                                              HTTP (requests)
                                                                     │
                                                              Jira Cloud REST API
```

---

## Jira Setup Notes

### Finding your Board ID
1. Go to your Jira project → Backlog or Board view
2. Look at the URL: `.../jira/software/projects/PROJ/boards/42` — `42` is the board ID
3. Or use the `get_boards` tool with your project key

### Finding custom field IDs
If the default custom field IDs don't work for your instance:
1. In Jira, go to **Settings → Issues → Custom fields**
2. Click on the field and note the ID in the URL (`customfield_XXXXX`)
3. Set the appropriate `JIRA_*_FIELD_ID` environment variable

### Classic vs Next-gen projects
| Feature | Classic (Company-managed) | Next-gen (Team-managed) |
|---|---|---|
| Epic link field | `customfield_10014` (string key) | Set `JIRA_EPIC_LINK_FIELD_ID=parent` |
| Sprints | Requires Scrum board | Built-in |
| Story points | `customfield_10016` | Usually `customfield_10016` or `story_points` |

### Atlassian Account IDs
Account IDs (used for assignee) look like `5b10ac8d82e34311xxxxxxxxxxx`. Find them with the `search_users` tool or in Jira's user profile URL.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| Claude doesn't show Jira tools | Check the config file path, ensure JSON is valid, restart Claude Desktop |
| `python` / `python3` not found | Add Python to PATH during installation (check "Add to PATH" in the Python installer) |
| `401 Unauthorized` | Verify `JIRA_EMAIL` and `JIRA_API_TOKEN` — token must be an API token, not your password |
| `403 Forbidden` | Your Atlassian account may not have permission to perform that action in the project |
| `404 Not Found` | Check `JIRA_BASE_URL` — must be `https://yourorg.atlassian.net` with no trailing slash |
| Sprint tools return 404 | Your board may not support sprints — ensure it is a Scrum board, not Kanban |
| Epic link not working | Try setting `JIRA_EPIC_LINK_FIELD_ID=parent` (Next-gen projects) |
| Story points not saving | Find the correct field ID for your instance and set `JIRA_STORY_POINTS_FIELD_ID` |
| `venv` activation fails | Re-run `python -m venv venv` inside the project folder, then activate |
| Tools work but sprint field is empty in `fetch_ticket` | Set `JIRA_SPRINT_FIELD_ID` to the correct custom field ID for your instance |

---

## Dependencies

```
mcp[cli]>=1.1.0    # Model Context Protocol framework
requests>=2.31.0   # HTTP client for Jira REST API calls
```

Install with: `pip install -r requirements.txt`

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-new-tool`
3. Make your changes in `api/jira_client.py` (API logic) and `tools/jira_tools.py` (tool definitions)
4. Test against a real Jira instance using `test_jira.py`
5. Open a pull request

---

## License

MIT — free to use, modify, and distribute.
