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
        observed_in: str = None
    ) -> str:
        """
        Creates a new Bug issue in Jira.
        
        Args:
            project_key: The uppercase key of the Jira project (e.g., 'ENG', 'PROJ').
            summary: A short, concise title for the bug.
            description: A detailed description of the bug.
            assignee_account_id: The Atlassian Account ID of the assignee (e.g., '5b10ac8d13...').
            observed_in: The environment, version, or place the bug was observed.
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})
            
        try:
            issue_data = jira_client.create_bug(project_key, summary, description, assignee_account_id, observed_in)
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
        assignee_account_id: str = None
    ) -> str:
        """
        Creates a new Story issue in Jira.
        
        Args:
            project_key: The uppercase key of the Jira project (e.g., 'ENG', 'PROJ').
            summary: A short, concise title for the story.
            description: A detailed description of the story.
            assignee_account_id: The Atlassian Account ID of the assignee (e.g., '5b10ac8d13...').
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})
            
        try:
            issue_data = jira_client.create_story(project_key, summary, description, assignee_account_id)
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
        assignee_account_id: str = None
    ) -> str:
        """
        Creates a new Task issue in Jira.
        
        Args:
            project_key: The uppercase key of the Jira project (e.g., 'ENG', 'PROJ').
            summary: A short, concise title for the task.
            description: A detailed description of the task.
            assignee_account_id: The Atlassian Account ID of the assignee (e.g., '5b10ac8d13...').
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})
            
        try:
            issue_data = jira_client.create_task(project_key, summary, description, assignee_account_id)
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
        assignee_account_id: str = None
    ) -> str:
        """
        Creates a new Epic issue in Jira.
        
        Args:
            project_key: The uppercase key of the Jira project (e.g., 'ENG', 'PROJ').
            summary: A short, concise title for the epic (often used as the 'Epic Name').
            description: A detailed description of the epic.
            assignee_account_id: The Atlassian Account ID of the assignee (e.g., '5b10ac8d13...').
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})
            
        try:
            issue_data = jira_client.create_epic(project_key, summary, description, assignee_account_id)
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
        Fetches a brief summary of a specific Jira ticket.
        
        Args:
            issue_key: The key of the Jira issue (e.g., 'PROJ-123') or the ticket number.
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            issue = jira_client.get_issue(issue_key)
            
            # Extract fields
            fields = issue.get("fields", {})
            summary = fields.get("summary", "No Summary")
            status = fields.get("status", {}).get("name", "Unknown")
            issue_type = fields.get("issuetype", {}).get("name", "Unknown")
            priority = fields.get("priority", {}).get("name", "Unknown")
            
            assignee = fields.get("assignee")
            assignee_name = assignee.get("displayName", "Unassigned") if assignee else "Unassigned"
            
            reporter = fields.get("reporter")
            reporter_name = reporter.get("displayName", "Unknown") if reporter else "Unknown"

            # Parse Jira doc format if description is missing or complex
            description_text = "No Description"
            desc_field = fields.get("description")
            
            if desc_field:
                if isinstance(desc_field, str):
                    description_text = desc_field
                elif isinstance(desc_field, dict) and "content" in desc_field:
                    # Simple ADF parsing
                    texts = []
                    for block in desc_field.get("content", []):
                        if block.get("type") == "paragraph":
                            paragraph_texts = [item.get("text", "") for item in block.get("content", []) if item.get("type") == "text"]
                            texts.append("".join(paragraph_texts))
                    if texts:
                        description_text = "\n".join(texts)
            
            creds = get_jira_credentials()
            issue_url = f"{creds['url']}/browse/{issue_key}"
            
            brief = {
                "key": issue_key,
                "url": issue_url,
                "type": issue_type,
                "summary": summary,
                "status": status,
                "priority": priority,
                "assignee": assignee_name,
                "reporter": reporter_name,
                "description": description_text
            }
            
            return json.dumps({
                "success": True,
                "brief": brief
            }, indent=2)
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
    def update_issue(issue_key: str, summary: str = None, description: str = None) -> str:
        """
        Updates the summary or description of a Jira issue.
        
        Args:
            issue_key: The key of the Jira issue (e.g., 'PROJ-123').
            summary: New summary for the issue (optional).
            description: New description for the issue (optional).
        """
        valid, msg = check_jira_credentials()
        if not valid:
            return json.dumps({"success": False, "error": msg})

        try:
            jira_client.update_issue(issue_key, summary, description)
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
    def transition_issue(issue_key: str, transition_id: str) -> str:
        """
        Transitions a Jira issue to a new status.
        
        Args:
            issue_key: The key of the Jira issue (e.g., 'PROJ-123').
            transition_id: The ID of the transition to apply.
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
