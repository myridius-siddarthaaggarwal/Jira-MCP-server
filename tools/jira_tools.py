import json
import requests
from config.settings import check_jira_credentials, get_jira_credentials
from api import jira_client

def format_error(e):
    error_msg = str(e)
    if isinstance(e, requests.exceptions.RequestException) and hasattr(e, 'response') and e.response is not None:
        try:
            error_details = e.response.json()
            error_msg += f" | Details: {json.dumps(error_details)}"
        except ValueError:
            error_msg += f" | Details: {e.response.text}"
    return json.dumps({"success": False, "error": error_msg}, indent=2)

def register_tools(mcp):
    
    @mcp.tool()
    def create_jira_bug(
        project_key: str,
        summary: str,
        description: str,
        assignee_account_id: str = None,
        observed_in: str = None,
        sprint_id: int = None,
        priority: str = None,
        labels: list = None,
        story_points: float = None,
        epic_key: str = None,
    ) -> str:
        """
        Creates a new Bug issue in Jira.

        Args:
            project_key: The uppercase key of the Jira project (e.g., 'ENG', 'PROJ').
            summary: A short, concise title for the bug.
            description: A detailed description of the bug.
            assignee_account_id: The Atlassian Account ID of the assignee (e.g., '5b10ac8d13...').
            observed_in: The environment, version, or place the bug was observed.
            sprint_id: Numeric ID of the sprint to add the bug to (use get_sprints to find IDs).
            priority: Priority name (e.g., 'Highest', 'High', 'Medium', 'Low', 'Lowest').
            labels: List of label strings to apply (e.g., ['backend', 'regression']).
            story_points: Story point estimate (e.g., 3.0).
            epic_key: Key of the parent Epic to link this bug to (e.g., 'PROJ-10').
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            issue_data = jira_client.create_bug(
                project_key, summary, description,
                assignee_account_id, observed_in,
                sprint_id, priority, labels, story_points, epic_key
            )
            issue_key = issue_data.get("key")
            creds = get_jira_credentials()
            issue_url = f"{creds['url']}/browse/{issue_key}"

            return json.dumps({
                "success": True,
                "message": f"Successfully created bug {issue_key}",
                "issue_key": issue_key,
                "url": issue_url
            }, indent=2)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def create_jira_story(
        project_key: str,
        summary: str,
        description: str = "",
        assignee_account_id: str = None,
        sprint_id: int = None,
        priority: str = None,
        labels: list = None,
        story_points: float = None,
        epic_key: str = None,
    ) -> str:
        """
        Creates a new Story issue in Jira.

        Args:
            project_key: The uppercase key of the Jira project (e.g., 'ENG', 'PROJ').
            summary: A short, concise title for the story.
            description: A detailed description of the story.
            assignee_account_id: The Atlassian Account ID of the assignee.
            sprint_id: Numeric ID of the sprint to add the story to.
            priority: Priority name (e.g., 'Highest', 'High', 'Medium', 'Low', 'Lowest').
            labels: List of label strings to apply.
            story_points: Story point estimate (e.g., 5.0).
            epic_key: Key of the parent Epic to link this story to (e.g., 'PROJ-10').
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            issue_data = jira_client.create_story(
                project_key, summary, description,
                assignee_account_id, sprint_id, priority, labels, story_points, epic_key
            )
            issue_key = issue_data.get("key")
            creds = get_jira_credentials()
            issue_url = f"{creds['url']}/browse/{issue_key}"

            return json.dumps({
                "success": True,
                "message": f"Successfully created story {issue_key}",
                "issue_key": issue_key,
                "url": issue_url
            }, indent=2)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def create_jira_task(
        project_key: str,
        summary: str,
        description: str = "",
        assignee_account_id: str = None,
        sprint_id: int = None,
        priority: str = None,
        labels: list = None,
        story_points: float = None,
        epic_key: str = None,
    ) -> str:
        """
        Creates a new Task issue in Jira.

        Args:
            project_key: The uppercase key of the Jira project (e.g., 'ENG', 'PROJ').
            summary: A short, concise title for the task.
            description: A detailed description of the task.
            assignee_account_id: The Atlassian Account ID of the assignee.
            sprint_id: Numeric ID of the sprint to add the task to.
            priority: Priority name (e.g., 'Highest', 'High', 'Medium', 'Low', 'Lowest').
            labels: List of label strings to apply.
            story_points: Story point estimate (e.g., 2.0).
            epic_key: Key of the parent Epic to link this task to (e.g., 'PROJ-10').
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            issue_data = jira_client.create_task(
                project_key, summary, description,
                assignee_account_id, sprint_id, priority, labels, story_points, epic_key
            )
            issue_key = issue_data.get("key")
            creds = get_jira_credentials()
            issue_url = f"{creds['url']}/browse/{issue_key}"

            return json.dumps({
                "success": True,
                "message": f"Successfully created task {issue_key}",
                "issue_key": issue_key,
                "url": issue_url
            }, indent=2)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def create_jira_epic(
        project_key: str,
        summary: str,
        description: str = "",
        assignee_account_id: str = None,
        sprint_id: int = None,
        priority: str = None,
        labels: list = None,
        story_points: float = None,
    ) -> str:
        """
        Creates a new Epic issue in Jira.

        Args:
            project_key: The uppercase key of the Jira project (e.g., 'ENG', 'PROJ').
            summary: A short, concise title for the epic (used as the Epic Name).
            description: A detailed description of the epic.
            assignee_account_id: The Atlassian Account ID of the assignee.
            sprint_id: Numeric ID of the sprint to associate the epic with.
            priority: Priority name (e.g., 'Highest', 'High', 'Medium', 'Low', 'Lowest').
            labels: List of label strings to apply.
            story_points: Story point estimate for the epic.
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            issue_data = jira_client.create_epic(
                project_key, summary, description,
                assignee_account_id, sprint_id, priority, labels, story_points
            )
            issue_key = issue_data.get("key")
            creds = get_jira_credentials()
            issue_url = f"{creds['url']}/browse/{issue_key}"

            return json.dumps({
                "success": True,
                "message": f"Successfully created epic {issue_key}",
                "issue_key": issue_key,
                "url": issue_url
            }, indent=2)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_issue(issue_key: str) -> str:
        """
        Retrieves details for a specific Jira issue.
        
        Args:
            issue_key: The key of the Jira issue (e.g., 'PROJ-123').
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            issue = jira_client.get_issue(issue_key)
            return json.dumps({
                "success": True,
                "issue": issue
            }, indent=2)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def fetch_ticket(issue_key: str) -> str:
        """
        Fetches a human-readable summary of a specific Jira ticket including
        status, assignee, priority, sprint, story points, labels, and description.

        Args:
            issue_key: The key of the Jira issue (e.g., 'PROJ-123').
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            issue = jira_client.get_issue(issue_key)
            creds = get_jira_credentials()
            fields = issue.get("fields", {})

            summary = fields.get("summary", "No Summary")
            status = fields.get("status", {}).get("name", "Unknown")
            issue_type = fields.get("issuetype", {}).get("name", "Unknown")
            priority = fields.get("priority", {}).get("name", "Unknown")
            labels = fields.get("labels", [])
            created = fields.get("created", "")
            updated = fields.get("updated", "")

            assignee = fields.get("assignee")
            assignee_name = assignee.get("displayName", "Unassigned") if assignee else "Unassigned"
            assignee_id = assignee.get("accountId") if assignee else None

            reporter = fields.get("reporter")
            reporter_name = reporter.get("displayName", "Unknown") if reporter else "Unknown"

            # Story points
            story_points = fields.get(creds["story_points_field_id"])

            # Sprint — sprint field is a list of sprint objects in ADF
            sprint_name = None
            sprint_id = None
            raw_sprint = fields.get(creds["sprint_field_id"])
            if isinstance(raw_sprint, list) and raw_sprint:
                active = next((s for s in raw_sprint if s.get("state") == "active"), raw_sprint[-1])
                sprint_name = active.get("name")
                sprint_id = active.get("id")
            elif isinstance(raw_sprint, dict):
                sprint_name = raw_sprint.get("name")
                sprint_id = raw_sprint.get("id")

            # Epic link (classic or next-gen parent)
            epic_key_val = fields.get(creds["epic_link_field_id"])
            if not epic_key_val:
                parent = fields.get("parent")
                if parent:
                    epic_key_val = parent.get("key")

            # Parse ADF description
            description_text = "No Description"
            desc_field = fields.get("description")
            if desc_field:
                if isinstance(desc_field, str):
                    description_text = desc_field
                elif isinstance(desc_field, dict) and "content" in desc_field:
                    texts = []
                    for block in desc_field.get("content", []):
                        if block.get("type") == "paragraph":
                            paragraph_texts = [
                                item.get("text", "")
                                for item in block.get("content", [])
                                if item.get("type") == "text"
                            ]
                            texts.append("".join(paragraph_texts))
                    description_text = "\n".join(texts) if texts else "No Description"

            issue_url = f"{creds['url']}/browse/{issue_key}"

            brief = {
                "key": issue_key,
                "url": issue_url,
                "type": issue_type,
                "summary": summary,
                "status": status,
                "priority": priority,
                "assignee": assignee_name,
                "assignee_account_id": assignee_id,
                "reporter": reporter_name,
                "labels": labels,
                "story_points": story_points,
                "sprint": {"id": sprint_id, "name": sprint_name} if sprint_name else None,
                "epic_key": epic_key_val,
                "created": created,
                "updated": updated,
                "description": description_text,
            }

            return json.dumps({"success": True, "brief": brief}, indent=2)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def search_issues(jql: str, max_results: int = 10) -> str:
        """
        Searches for Jira issues using JQL (Jira Query Language).
        
        Args:
            jql: The Jira Query Language string (e.g., 'project = PROJ AND status = "In Progress"').
            max_results: The maximum number of issues to return (default 10).
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            results = jira_client.search_issues(jql, max_results)
            return json.dumps({
                "success": True,
                "results": results
            }, indent=2)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def find_tickets(assignee: str = None, status: str = None, name: str = None, max_results: int = 10) -> str:
        """
        Searches for Jira issues by assignee, status, and/or name.
        
        Args:
            assignee: The assignee's username, display name, account ID, or 'currentUser()'.
            status: The status name (e.g., 'In Progress', 'Done', ' Functional Sign-off').
            name: Text to search for in the summary, description, or comment.
            max_results: The maximum number of issues to return (default 80).
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            conditions = []
            if assignee:
                conditions.append(f'assignee = "{assignee}"')
            if status:
                conditions.append(f'status = "{status}"')
            if name:
                conditions.append(f'text ~ "{name}"')
                
            if not conditions:
                return json.dumps({"success": False, "error": "At least one search parameter (assignee, status, or name) must be provided."})
                
            jql = " AND ".join(conditions)
            results = jira_client.search_issues(jql, max_results)
            return json.dumps({
                "success": True,
                "jql_used": jql,
                "results": results
            }, indent=2)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def update_issue(
        issue_key: str,
        summary: str = None,
        description: str = None,
        assignee_account_id: str = None,
        priority: str = None,
        labels: list = None,
        story_points: float = None,
        sprint_id: int = None,
        epic_key: str = None,
        status_name: str = None,
    ) -> str:
        """
        Updates one or more fields of any Jira issue (Bug, Story, Task, Epic, etc.).

        Args:
            issue_key: The key of the Jira issue to update (e.g., 'PROJ-123').
            summary: New summary/title for the issue.
            description: New description for the issue.
            assignee_account_id: Atlassian Account ID of the new assignee.
                                 Pass empty string '' to unassign.
            priority: New priority (e.g., 'Highest', 'High', 'Medium', 'Low', 'Lowest').
            labels: New list of labels — replaces existing labels entirely (e.g., ['backend', 'urgent']).
            story_points: New story point estimate (e.g., 5.0).
            sprint_id: Numeric ID of the sprint to move the issue to.
            epic_key: Key of the Epic to link this issue to (e.g., 'PROJ-10').
            status_name: Target status name to transition to (e.g., 'In Progress', 'Done').
                         Use get_issue_transitions to see available transitions for the issue.
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            jira_client.update_issue(
                issue_key, summary, description, assignee_account_id,
                priority, labels, story_points, sprint_id, epic_key, status_name
            )
            return json.dumps({
                "success": True,
                "message": f"Successfully updated issue {issue_key}"
            }, indent=2)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def add_comment(issue_key: str, comment_text: str) -> str:
        """
        Adds a comment to a Jira issue.

        Args:
            issue_key: The key of the Jira issue (e.g., 'PROJ-123').
            comment_text: The text of the comment to add.
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            comment = jira_client.add_comment(issue_key, comment_text)
            return json.dumps({
                "success": True,
                "message": f"Successfully added comment to {issue_key}",
                "comment": comment
            }, indent=2)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_issue_transitions(issue_key: str) -> str:
        """
        Lists all available status transitions for a Jira issue.

        Use this to discover valid transition names before calling
        transition_issue or update_issue (status_name parameter).

        Args:
            issue_key: The key of the Jira issue (e.g., 'PROJ-123').
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            transitions = jira_client.get_issue_transitions(issue_key)
            simplified = [
                {"id": t["id"], "name": t["name"]}
                for t in transitions
            ]
            return json.dumps({
                "success": True,
                "issue_key": issue_key,
                "transitions": simplified
            }, indent=2)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def transition_issue(issue_key: str, transition_id: str) -> str:
        """
        Transitions a Jira issue to a new status using a numeric transition ID.

        To apply a transition by name instead, use update_issue with the
        status_name parameter. Use get_issue_transitions to list available IDs.

        Args:
            issue_key: The key of the Jira issue (e.g., 'PROJ-123').
            transition_id: The numeric ID of the transition to apply (e.g., '31').
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            jira_client.transition_issue(issue_key, transition_id)
            return json.dumps({
                "success": True,
                "message": f"Successfully transitioned issue {issue_key}"
            }, indent=2)
        except Exception as e:
            return format_error(e)

    # -------------------------------------------------------------------------
    # Sprint / Board Tools
    # -------------------------------------------------------------------------

    @mcp.tool()
    def get_boards(project_key: str = None) -> str:
        """
        Lists all Agile boards, optionally filtered by project.

        Args:
            project_key: Filter boards to a specific project (e.g., 'PROJ').
                         Leave empty to list all visible boards.
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            data = jira_client.get_boards(project_key)
            boards = [
                {"id": b["id"], "name": b["name"], "type": b["type"]}
                for b in data.get("values", [])
            ]
            return json.dumps({"success": True, "boards": boards}, indent=2)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_sprints(board_id: int, state: str = None) -> str:
        """
        Lists sprints for a given Agile board.

        Args:
            board_id: Numeric ID of the Agile board (use get_boards to find IDs).
            state: Filter by sprint state: 'active', 'future', or 'closed'.
                   Leave empty to return all sprints.
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            data = jira_client.get_sprints(board_id, state)
            sprints = [
                {
                    "id": s["id"],
                    "name": s["name"],
                    "state": s["state"],
                    "startDate": s.get("startDate"),
                    "endDate": s.get("endDate"),
                    "goal": s.get("goal", ""),
                }
                for s in data.get("values", [])
            ]
            return json.dumps({"success": True, "sprints": sprints}, indent=2)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_active_sprint(board_id: int) -> str:
        """
        Returns the currently active sprint for a given board.

        Args:
            board_id: Numeric ID of the Agile board (use get_boards to find IDs).
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            sprint = jira_client.get_active_sprint(board_id)
            if not sprint:
                return json.dumps({
                    "success": True,
                    "message": "No active sprint found for this board.",
                    "sprint": None
                }, indent=2)
            return json.dumps({
                "success": True,
                "sprint": {
                    "id": sprint["id"],
                    "name": sprint["name"],
                    "state": sprint["state"],
                    "startDate": sprint.get("startDate"),
                    "endDate": sprint.get("endDate"),
                    "goal": sprint.get("goal", ""),
                }
            }, indent=2)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def create_sprint(
        board_id: int,
        name: str,
        goal: str = None,
        start_date: str = None,
        end_date: str = None,
    ) -> str:
        """
        Creates a new sprint on an Agile board.

        Args:
            board_id: Numeric ID of the board to create the sprint on (use get_boards to find IDs).
            name: Name for the new sprint (e.g., 'Sprint 12').
            goal: Optional sprint goal description.
            start_date: Optional start date in ISO 8601 format (e.g., '2026-04-14T00:00:00.000Z').
            end_date: Optional end date in ISO 8601 format (e.g., '2026-04-28T00:00:00.000Z').
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            sprint = jira_client.create_sprint(board_id, name, goal, start_date, end_date)
            return json.dumps({
                "success": True,
                "message": f"Successfully created sprint '{name}'",
                "sprint": {
                    "id": sprint["id"],
                    "name": sprint["name"],
                    "state": sprint.get("state"),
                    "startDate": sprint.get("startDate"),
                    "endDate": sprint.get("endDate"),
                    "goal": sprint.get("goal", ""),
                }
            }, indent=2)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def add_issues_to_sprint(sprint_id: int, issue_keys: list) -> str:
        """
        Adds one or more Jira issues to a sprint.

        Args:
            sprint_id: Numeric ID of the target sprint (use get_sprints to find IDs).
            issue_keys: List of issue keys to add (e.g., ['PROJ-1', 'PROJ-2']).
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        if not issue_keys:
            return json.dumps({"success": False, "error": "issue_keys must be a non-empty list."})

        try:
            jira_client.add_issues_to_sprint(sprint_id, issue_keys)
            return json.dumps({
                "success": True,
                "message": f"Successfully added {len(issue_keys)} issue(s) to sprint {sprint_id}",
                "added_issues": issue_keys,
                "sprint_id": sprint_id
            }, indent=2)
        except Exception as e:
            return format_error(e)

    # -------------------------------------------------------------------------
    # Comment Tools
    # -------------------------------------------------------------------------

    @mcp.tool()
    def get_comments(issue_key: str, max_results: int = 50) -> str:
        """
        Lists all comments on a Jira issue.

        Args:
            issue_key: The key of the Jira issue (e.g., 'PROJ-123').
            max_results: Maximum number of comments to return (default 50).
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            data = jira_client.get_comments(issue_key, max_results)
            comments = []
            for c in data.get("comments", []):
                author = c.get("author", {})
                # Extract plain text from ADF body
                body_text = ""
                body = c.get("body", {})
                if isinstance(body, str):
                    body_text = body
                elif isinstance(body, dict):
                    for block in body.get("content", []):
                        if block.get("type") == "paragraph":
                            body_text += "".join(
                                item.get("text", "")
                                for item in block.get("content", [])
                                if item.get("type") == "text"
                            ) + "\n"
                    body_text = body_text.strip()
                comments.append({
                    "id": c.get("id"),
                    "author": author.get("displayName", "Unknown"),
                    "author_account_id": author.get("accountId"),
                    "created": c.get("created"),
                    "updated": c.get("updated"),
                    "body": body_text,
                })
            return json.dumps({
                "success": True,
                "issue_key": issue_key,
                "total": data.get("total", len(comments)),
                "comments": comments,
            }, indent=2)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def update_comment(issue_key: str, comment_id: str, comment_text: str) -> str:
        """
        Edits the text of an existing comment on a Jira issue.

        Args:
            issue_key: The key of the Jira issue (e.g., 'PROJ-123').
            comment_id: The numeric ID of the comment to edit (use get_comments to find IDs).
            comment_text: The new text for the comment.
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            result = jira_client.update_comment(issue_key, comment_id, comment_text)
            return json.dumps({
                "success": True,
                "message": f"Successfully updated comment {comment_id} on {issue_key}",
                "comment_id": result.get("id"),
            }, indent=2)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def delete_comment(issue_key: str, comment_id: str) -> str:
        """
        Deletes a comment from a Jira issue. This action is irreversible.

        Args:
            issue_key: The key of the Jira issue (e.g., 'PROJ-123').
            comment_id: The numeric ID of the comment to delete (use get_comments to find IDs).
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            jira_client.delete_comment(issue_key, comment_id)
            return json.dumps({
                "success": True,
                "message": f"Successfully deleted comment {comment_id} from {issue_key}",
            }, indent=2)
        except Exception as e:
            return format_error(e)

    # -------------------------------------------------------------------------
    # Worklog Tools
    # -------------------------------------------------------------------------

    @mcp.tool()
    def get_worklogs(issue_key: str) -> str:
        """
        Lists all time-logged worklogs for a Jira issue.

        Args:
            issue_key: The key of the Jira issue (e.g., 'PROJ-123').
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            data = jira_client.get_worklogs(issue_key)
            worklogs = []
            for w in data.get("worklogs", []):
                author = w.get("author", {})
                worklogs.append({
                    "id": w.get("id"),
                    "author": author.get("displayName", "Unknown"),
                    "author_account_id": author.get("accountId"),
                    "time_spent": w.get("timeSpent"),
                    "time_spent_seconds": w.get("timeSpentSeconds"),
                    "started": w.get("started"),
                    "created": w.get("created"),
                })
            return json.dumps({
                "success": True,
                "issue_key": issue_key,
                "total_worklogs": data.get("total", len(worklogs)),
                "worklogs": worklogs,
            }, indent=2)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def add_worklog(
        issue_key: str,
        time_spent: str,
        started: str = None,
        comment: str = None,
    ) -> str:
        """
        Logs time spent working on a Jira issue.

        Args:
            issue_key: The key of the Jira issue (e.g., 'PROJ-123').
            time_spent: Time spent string (e.g., '2h', '1d', '30m', '1h 30m').
            started: When the work started — ISO 8601 datetime
                     (e.g., '2026-04-10T09:00:00.000+0000'). Defaults to now if omitted.
            comment: Optional description of the work done.
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            result = jira_client.add_worklog(issue_key, time_spent, started, comment)
            return json.dumps({
                "success": True,
                "message": f"Successfully logged {time_spent} on {issue_key}",
                "worklog_id": result.get("id"),
                "time_spent": result.get("timeSpent"),
            }, indent=2)
        except Exception as e:
            return format_error(e)

    # -------------------------------------------------------------------------
    # Assignment & Linking Tools
    # -------------------------------------------------------------------------

    @mcp.tool()
    def assign_issue(issue_key: str, assignee_account_id: str) -> str:
        """
        Assigns a Jira issue to a user. Pass empty string to unassign.

        Args:
            issue_key: The key of the Jira issue (e.g., 'PROJ-123').
            assignee_account_id: The Atlassian Account ID of the new assignee.
                                 Pass empty string '' to unassign the issue.
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            jira_client.assign_issue(issue_key, assignee_account_id)
            action = "Unassigned" if not assignee_account_id else f"Assigned to {assignee_account_id}"
            return json.dumps({
                "success": True,
                "message": f"{action} issue {issue_key}",
            }, indent=2)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_issue_link_types() -> str:
        """
        Lists all available issue link types in Jira (e.g., 'Blocks', 'Clones', 'Relates to').

        Use the link type names returned here when calling link_issues.
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            link_types = jira_client.get_issue_link_types()
            simplified = [
                {
                    "id": lt.get("id"),
                    "name": lt.get("name"),
                    "inward": lt.get("inward"),
                    "outward": lt.get("outward"),
                }
                for lt in link_types
            ]
            return json.dumps({"success": True, "link_types": simplified}, indent=2)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def link_issues(
        inward_issue_key: str,
        outward_issue_key: str,
        link_type_name: str,
    ) -> str:
        """
        Creates a directional link between two Jira issues.

        Examples: 'PROJ-1 blocks PROJ-2', 'PROJ-3 clones PROJ-4', 'PROJ-5 relates to PROJ-6'.
        Use get_issue_link_types to discover exact link type names.

        Args:
            inward_issue_key: The issue on the inward side of the link (e.g., 'PROJ-1').
            outward_issue_key: The issue on the outward side of the link (e.g., 'PROJ-2').
            link_type_name: The link type (e.g., 'Blocks', 'Clones', 'Duplicate', 'Relates to').
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            jira_client.link_issues(inward_issue_key, outward_issue_key, link_type_name)
            return json.dumps({
                "success": True,
                "message": f"Successfully linked {inward_issue_key} → {outward_issue_key} ({link_type_name})",
            }, indent=2)
        except Exception as e:
            return format_error(e)

    # -------------------------------------------------------------------------
    # Sprint Management Tools
    # -------------------------------------------------------------------------

    @mcp.tool()
    def update_sprint(
        sprint_id: int,
        name: str = None,
        state: str = None,
        goal: str = None,
        start_date: str = None,
        end_date: str = None,
    ) -> str:
        """
        Updates a sprint's properties, or starts/completes it.

        To start a sprint: set state='active'.
        To complete a sprint: set state='closed'.

        Args:
            sprint_id: Numeric ID of the sprint to update (use get_sprints to find IDs).
            name: New name for the sprint.
            state: New state — 'active' to start, 'closed' to complete, 'future' to reopen.
            goal: Updated sprint goal description.
            start_date: New start date in ISO 8601 (e.g., '2026-04-14T00:00:00.000Z').
            end_date: New end date in ISO 8601 (e.g., '2026-04-28T00:00:00.000Z').
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            result = jira_client.update_sprint(sprint_id, name, state, goal, start_date, end_date)
            return json.dumps({
                "success": True,
                "message": f"Successfully updated sprint {sprint_id}",
                "sprint": {
                    "id": result.get("id"),
                    "name": result.get("name"),
                    "state": result.get("state"),
                    "startDate": result.get("startDate"),
                    "endDate": result.get("endDate"),
                    "goal": result.get("goal", ""),
                },
            }, indent=2)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def remove_issues_from_sprint(issue_keys: list) -> str:
        """
        Moves one or more issues to the backlog, removing them from any sprint.

        Args:
            issue_keys: List of issue keys to move to backlog (e.g., ['PROJ-1', 'PROJ-2']).
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        if not issue_keys:
            return json.dumps({"success": False, "error": "issue_keys must be a non-empty list."})

        try:
            jira_client.remove_issue_from_sprint(issue_keys)
            return json.dumps({
                "success": True,
                "message": f"Successfully moved {len(issue_keys)} issue(s) to backlog",
                "issues": issue_keys,
            }, indent=2)
        except Exception as e:
            return format_error(e)

    # -------------------------------------------------------------------------
    # Discovery / Metadata Tools
    # -------------------------------------------------------------------------

    @mcp.tool()
    def get_project_info(project_key: str) -> str:
        """
        Returns metadata about a Jira project — name, description, lead,
        project type, available issue types, and components.

        Args:
            project_key: The uppercase project key (e.g., 'PROJ').
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            proj = jira_client.get_project_info(project_key)
            creds = get_jira_credentials()
            return json.dumps({
                "success": True,
                "project": {
                    "key": proj.get("key"),
                    "name": proj.get("name"),
                    "description": proj.get("description", ""),
                    "project_type": proj.get("projectTypeKey"),
                    "lead": proj.get("lead", {}).get("displayName"),
                    "url": f"{creds['url']}/jira/software/projects/{proj.get('key')}/boards",
                    "issue_types": [
                        {"id": it.get("id"), "name": it.get("name")}
                        for it in proj.get("issueTypes", [])
                    ],
                    "components": [
                        {"id": c.get("id"), "name": c.get("name")}
                        for c in proj.get("components", [])
                    ],
                },
            }, indent=2)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_issue_types(project_key: str) -> str:
        """
        Lists all issue types available in a Jira project (Bug, Story, Task, Epic, etc.)

        Args:
            project_key: The uppercase project key (e.g., 'PROJ').
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            issue_types = jira_client.get_issue_types(project_key)
            simplified = [
                {"id": it.get("id"), "name": it.get("name"), "subtask": it.get("subtask", False)}
                for it in issue_types
            ]
            return json.dumps({
                "success": True,
                "project_key": project_key,
                "issue_types": simplified,
            }, indent=2)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_priorities() -> str:
        """
        Lists all priority levels configured in Jira (e.g., Highest, High, Medium, Low, Lowest).

        Use the priority names returned here in create/update tools.
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            priorities = jira_client.get_priorities()
            simplified = [
                {"id": p.get("id"), "name": p.get("name")}
                for p in priorities
            ]
            return json.dumps({"success": True, "priorities": simplified}, indent=2)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def search_users(
        query: str,
        project_key: str = None,
        max_results: int = 20,
    ) -> str:
        """
        Searches for Jira users by name or email address.

        Returns account IDs that can be used with assignee fields.

        Args:
            query: Name or email fragment to search for (e.g., 'john', 'john@example.com').
            project_key: Optional — restrict results to users assignable to this project.
            max_results: Maximum number of users to return (default 20).
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            users = jira_client.search_users(query, project_key, max_results)
            simplified = [
                {
                    "account_id": u.get("accountId"),
                    "display_name": u.get("displayName"),
                    "email": u.get("emailAddress", ""),
                    "active": u.get("active", True),
                }
                for u in users
            ]
            return json.dumps({
                "success": True,
                "query": query,
                "users": simplified,
            }, indent=2)
        except Exception as e:
            return format_error(e)
