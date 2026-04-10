import requests
from config.settings import check_jira_credentials, get_jira_credentials

def build_headers():
    return {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

def get_auth():
    creds = get_jira_credentials()
    return (creds["email"], creds["token"])

def _create_basic_issue(
    project_key: str,
    issue_type: str,
    summary: str,
    description: str,
    assignee_id: str = None,
    extra_fields: dict = None,
    sprint_id: int = None,
    priority: str = None,
    labels: list = None,
    story_points: float = None,
    epic_key: str = None,
):
    creds = get_jira_credentials()
    url = f"{creds['url']}/rest/api/3/issue"

    fields = {
        "project": {"key": project_key},
        "summary": summary,
        "issuetype": {"name": issue_type}
    }

    if description:
        fields["description"] = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"text": description, "type": "text"}]
                }
            ]
        }

    if assignee_id:
        fields["assignee"] = {"id": assignee_id}

    if priority:
        fields["priority"] = {"name": priority}

    if labels:
        fields["labels"] = labels

    if story_points is not None:
        fields[creds["story_points_field_id"]] = story_points

    if sprint_id is not None:
        fields[creds["sprint_field_id"]] = sprint_id

    if epic_key and issue_type != "Epic":
        epic_field_id = creds["epic_link_field_id"]
        if epic_field_id == "parent":
            fields["parent"] = {"key": epic_key}
        else:
            fields[epic_field_id] = epic_key

    if extra_fields:
        fields.update(extra_fields)

    payload = {"fields": fields}

    response = requests.post(url, json=payload, headers=build_headers(), auth=get_auth())
    response.raise_for_status()
    return response.json()

def create_bug(
    project_key: str,
    summary: str,
    description: str,
    assignee_id: str = None,
    observed_in: str = None,
    sprint_id: int = None,
    priority: str = None,
    labels: list = None,
    story_points: float = None,
    epic_key: str = None,
):
    creds = get_jira_credentials()
    extra_fields = {}
    if observed_in and creds.get("observed_in_field_id"):
        extra_fields[creds["observed_in_field_id"]] = {"value": observed_in}
    return _create_basic_issue(
        project_key, "Bug", summary, description,
        assignee_id, extra_fields, sprint_id, priority, labels, story_points, epic_key
    )


def create_story(
    project_key: str,
    summary: str,
    description: str,
    assignee_id: str = None,
    sprint_id: int = None,
    priority: str = None,
    labels: list = None,
    story_points: float = None,
    epic_key: str = None,
):
    return _create_basic_issue(
        project_key, "Story", summary, description,
        assignee_id, None, sprint_id, priority, labels, story_points, epic_key
    )


def create_task(
    project_key: str,
    summary: str,
    description: str,
    assignee_id: str = None,
    sprint_id: int = None,
    priority: str = None,
    labels: list = None,
    story_points: float = None,
    epic_key: str = None,
):
    return _create_basic_issue(
        project_key, "Task", summary, description,
        assignee_id, None, sprint_id, priority, labels, story_points, epic_key
    )


def create_epic(
    project_key: str,
    summary: str,
    description: str,
    assignee_id: str = None,
    sprint_id: int = None,
    priority: str = None,
    labels: list = None,
    story_points: float = None,
):
    return _create_basic_issue(
        project_key, "Epic", summary, description,
        assignee_id, None, sprint_id, priority, labels, story_points
    )

def get_issue(issue_key: str):
    creds = get_jira_credentials()
    url = f"{creds['url']}/rest/api/3/issue/{issue_key}"
    response = requests.get(url, headers=build_headers(), auth=get_auth())
    response.raise_for_status()
    return response.json()

def search_issues(jql: str, max_results: int = 10):
    creds = get_jira_credentials()
    url = f"{creds['url']}/rest/api/3/search"
    payload = {
        "jql": jql,
        "maxResults": max_results,
        "fields": [
            "summary", "status", "assignee", "reporter", "priority",
            "issuetype", "created", "updated", "labels", "description",
            creds["story_points_field_id"],
            creds["sprint_field_id"],
        ]
    }
    response = requests.post(url, json=payload, headers=build_headers(), auth=get_auth())
    response.raise_for_status()
    return response.json()

def update_issue(
    issue_key: str,
    summary: str = None,
    description: str = None,
    assignee_id: str = None,
    priority: str = None,
    labels: list = None,
    story_points: float = None,
    sprint_id: int = None,
    epic_key: str = None,
    status_name: str = None,
):
    creds = get_jira_credentials()
    url = f"{creds['url']}/rest/api/3/issue/{issue_key}"

    fields = {}
    if summary:
        fields["summary"] = summary

    if description:
        fields["description"] = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"text": description, "type": "text"}]
                }
            ]
        }

    if assignee_id is not None:
        # Pass empty string to unassign
        fields["assignee"] = {"id": assignee_id} if assignee_id else None

    if priority:
        fields["priority"] = {"name": priority}

    if labels is not None:
        fields["labels"] = labels

    if story_points is not None:
        fields[creds["story_points_field_id"]] = story_points

    if sprint_id is not None:
        fields[creds["sprint_field_id"]] = sprint_id

    if epic_key is not None:
        epic_field_id = creds["epic_link_field_id"]
        if epic_field_id == "parent":
            fields["parent"] = {"key": epic_key} if epic_key else None
        else:
            fields[epic_field_id] = epic_key

    if not fields and status_name is None:
        raise ValueError("No fields to update.")

    if fields:
        payload = {"fields": fields}
        response = requests.put(url, json=payload, headers=build_headers(), auth=get_auth())
        response.raise_for_status()

    if status_name:
        _transition_by_name(issue_key, status_name)

    return {"success": True}

def add_comment(issue_key: str, comment_text: str):
    creds = get_jira_credentials()
    url = f"{creds['url']}/rest/api/3/issue/{issue_key}/comment"
    
    payload = {
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"text": comment_text, "type": "text"}]
                }
            ]
        }
    }
    
    response = requests.post(url, json=payload, headers=build_headers(), auth=get_auth())
    response.raise_for_status()
    return response.json()

def transition_issue(issue_key: str, transition_id: str):
    creds = get_jira_credentials()
    url = f"{creds['url']}/rest/api/3/issue/{issue_key}/transitions"

    payload = {
        "transition": {
            "id": transition_id
        }
    }

    response = requests.post(url, json=payload, headers=build_headers(), auth=get_auth())
    response.raise_for_status()
    if response.status_code == 204:
        return {"success": True}
    return response.json() if response.text else {"success": True}


def get_issue_transitions(issue_key: str):
    """Returns the list of available transitions for an issue."""
    creds = get_jira_credentials()
    url = f"{creds['url']}/rest/api/3/issue/{issue_key}/transitions"
    response = requests.get(url, headers=build_headers(), auth=get_auth())
    response.raise_for_status()
    return response.json().get("transitions", [])


def _transition_by_name(issue_key: str, status_name: str):
    """Resolve a status name to a transition ID and apply it."""
    transitions = get_issue_transitions(issue_key)
    match = next(
        (t for t in transitions if t["name"].lower() == status_name.lower()),
        None
    )
    if not match:
        available = [t["name"] for t in transitions]
        raise ValueError(f"Transition '{status_name}' not found. Available: {available}")
    transition_issue(issue_key, match["id"])


# ---------------------------------------------------------------------------
# Agile / Sprint API  (uses /rest/agile/1.0/ endpoint)
# ---------------------------------------------------------------------------

def get_boards(project_key: str = None):
    """List all Agile boards, optionally filtered by project key."""
    creds = get_jira_credentials()
    url = f"{creds['url']}/rest/agile/1.0/board"
    params = {}
    if project_key:
        params["projectKeyOrId"] = project_key
    response = requests.get(url, params=params, headers=build_headers(), auth=get_auth())
    response.raise_for_status()
    return response.json()


def get_sprints(board_id: int, state: str = None):
    """
    List sprints for a board.
    state: 'active', 'future', 'closed', or None for all.
    """
    creds = get_jira_credentials()
    url = f"{creds['url']}/rest/agile/1.0/board/{board_id}/sprint"
    params = {}
    if state:
        params["state"] = state
    response = requests.get(url, params=params, headers=build_headers(), auth=get_auth())
    response.raise_for_status()
    return response.json()


def get_active_sprint(board_id: int):
    """Return the single active sprint for a board, or None."""
    data = get_sprints(board_id, state="active")
    sprints = data.get("values", [])
    return sprints[0] if sprints else None


def create_sprint(
    board_id: int,
    name: str,
    goal: str = None,
    start_date: str = None,
    end_date: str = None,
):
    """
    Create a new sprint on a board.
    start_date / end_date: ISO 8601 strings e.g. '2026-04-14T00:00:00.000Z' (optional).
    """
    creds = get_jira_credentials()
    url = f"{creds['url']}/rest/agile/1.0/sprint"
    payload = {
        "name": name,
        "originBoardId": board_id,
    }
    if goal:
        payload["goal"] = goal
    if start_date:
        payload["startDate"] = start_date
    if end_date:
        payload["endDate"] = end_date
    response = requests.post(url, json=payload, headers=build_headers(), auth=get_auth())
    response.raise_for_status()
    return response.json()


def add_issues_to_sprint(sprint_id: int, issue_keys: list):
    """
    Move one or more issues into a sprint.
    issue_keys: list of issue key strings e.g. ['PROJ-1', 'PROJ-2'].
    """
    creds = get_jira_credentials()
    url = f"{creds['url']}/rest/agile/1.0/sprint/{sprint_id}/issue"
    payload = {"issues": issue_keys}
    response = requests.post(url, json=payload, headers=build_headers(), auth=get_auth())
    response.raise_for_status()
    if response.status_code == 204:
        return {"success": True}
    return response.json() if response.text else {"success": True}


def update_sprint(
    sprint_id: int,
    name: str = None,
    state: str = None,
    goal: str = None,
    start_date: str = None,
    end_date: str = None,
):
    """
    Update sprint properties or change its state.
    state: 'active' to start, 'closed' to complete.
    """
    creds = get_jira_credentials()
    url = f"{creds['url']}/rest/agile/1.0/sprint/{sprint_id}"
    payload = {}
    if name is not None:
        payload["name"] = name
    if state is not None:
        payload["state"] = state
    if goal is not None:
        payload["goal"] = goal
    if start_date is not None:
        payload["startDate"] = start_date
    if end_date is not None:
        payload["endDate"] = end_date
    if not payload:
        raise ValueError("No fields to update for sprint.")
    response = requests.put(url, json=payload, headers=build_headers(), auth=get_auth())
    response.raise_for_status()
    return response.json() if response.text else {"success": True}


def remove_issue_from_sprint(issue_keys: list):
    """
    Move one or more issues to the backlog (removes them from any sprint).
    issue_keys: list of issue key strings e.g. ['PROJ-1', 'PROJ-2'].
    """
    creds = get_jira_credentials()
    url = f"{creds['url']}/rest/agile/1.0/backlog/issue"
    payload = {"issues": issue_keys}
    response = requests.post(url, json=payload, headers=build_headers(), auth=get_auth())
    response.raise_for_status()
    if response.status_code == 204:
        return {"success": True}
    return response.json() if response.text else {"success": True}


# ---------------------------------------------------------------------------
# Comment API
# ---------------------------------------------------------------------------

def get_comments(issue_key: str, max_results: int = 50):
    """List comments on an issue."""
    creds = get_jira_credentials()
    url = f"{creds['url']}/rest/api/3/issue/{issue_key}/comment"
    params = {"maxResults": max_results, "orderBy": "created"}
    response = requests.get(url, params=params, headers=build_headers(), auth=get_auth())
    response.raise_for_status()
    return response.json()


def update_comment(issue_key: str, comment_id: str, comment_text: str):
    """Edit the body of an existing comment."""
    creds = get_jira_credentials()
    url = f"{creds['url']}/rest/api/3/issue/{issue_key}/comment/{comment_id}"
    payload = {
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"text": comment_text, "type": "text"}]
                }
            ]
        }
    }
    response = requests.put(url, json=payload, headers=build_headers(), auth=get_auth())
    response.raise_for_status()
    return response.json()


def delete_comment(issue_key: str, comment_id: str):
    """Delete a comment from an issue."""
    creds = get_jira_credentials()
    url = f"{creds['url']}/rest/api/3/issue/{issue_key}/comment/{comment_id}"
    response = requests.delete(url, headers=build_headers(), auth=get_auth())
    response.raise_for_status()
    return {"success": True}


# ---------------------------------------------------------------------------
# Worklog API
# ---------------------------------------------------------------------------

def get_worklogs(issue_key: str):
    """List all worklogs for an issue."""
    creds = get_jira_credentials()
    url = f"{creds['url']}/rest/api/3/issue/{issue_key}/worklog"
    response = requests.get(url, headers=build_headers(), auth=get_auth())
    response.raise_for_status()
    return response.json()


def add_worklog(issue_key: str, time_spent: str, started: str = None, comment: str = None):
    """
    Log time spent on an issue.
    time_spent: e.g. '2h', '1d 4h', '30m'
    started: ISO 8601 datetime e.g. '2026-04-10T09:00:00.000+0000' (defaults to now if omitted)
    comment: optional work description
    """
    creds = get_jira_credentials()
    url = f"{creds['url']}/rest/api/3/issue/{issue_key}/worklog"
    payload = {"timeSpent": time_spent}
    if started:
        payload["started"] = started
    if comment:
        payload["comment"] = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"text": comment, "type": "text"}]
                }
            ]
        }
    response = requests.post(url, json=payload, headers=build_headers(), auth=get_auth())
    response.raise_for_status()
    return response.json()


# ---------------------------------------------------------------------------
# Assignment & Issue Linking
# ---------------------------------------------------------------------------

def assign_issue(issue_key: str, assignee_id: str):
    """
    Assign an issue to a user.
    Pass assignee_id=None or empty string to unassign.
    """
    creds = get_jira_credentials()
    url = f"{creds['url']}/rest/api/3/issue/{issue_key}/assignee"
    payload = {"accountId": assignee_id if assignee_id else None}
    response = requests.put(url, json=payload, headers=build_headers(), auth=get_auth())
    response.raise_for_status()
    return {"success": True}


def get_issue_link_types():
    """List all available issue link type names (e.g., 'Blocks', 'Clones', 'Relates to')."""
    creds = get_jira_credentials()
    url = f"{creds['url']}/rest/api/3/issueLinkType"
    response = requests.get(url, headers=build_headers(), auth=get_auth())
    response.raise_for_status()
    return response.json().get("issueLinkTypes", [])


def link_issues(inward_issue_key: str, outward_issue_key: str, link_type_name: str):
    """
    Create a link between two issues.
    link_type_name: e.g. 'Blocks', 'Clones', 'Duplicate', 'Relates to'
                   Use get_issue_link_types() to discover valid names.
    """
    creds = get_jira_credentials()
    url = f"{creds['url']}/rest/api/3/issueLink"
    payload = {
        "type": {"name": link_type_name},
        "inwardIssue": {"key": inward_issue_key},
        "outwardIssue": {"key": outward_issue_key},
    }
    response = requests.post(url, json=payload, headers=build_headers(), auth=get_auth())
    response.raise_for_status()
    return {"success": True}


# ---------------------------------------------------------------------------
# Discovery / Metadata helpers
# ---------------------------------------------------------------------------

def get_project_info(project_key: str):
    """Return project metadata including name, lead, issue types, and components."""
    creds = get_jira_credentials()
    url = f"{creds['url']}/rest/api/3/project/{project_key}"
    response = requests.get(url, headers=build_headers(), auth=get_auth())
    response.raise_for_status()
    return response.json()


def get_issue_types(project_key: str):
    """Return all issue types available in a specific project."""
    project = get_project_info(project_key)
    return project.get("issueTypes", [])


def get_priorities():
    """Return all priority levels configured in Jira."""
    creds = get_jira_credentials()
    url = f"{creds['url']}/rest/api/3/priority"
    response = requests.get(url, headers=build_headers(), auth=get_auth())
    response.raise_for_status()
    return response.json()


def search_users(query: str, project_key: str = None, max_results: int = 20):
    """
    Search for users by name/email.
    If project_key is provided, restricts to users assignable to that project.
    """
    creds = get_jira_credentials()
    if project_key:
        url = f"{creds['url']}/rest/api/3/user/assignable/search"
        params = {"project": project_key, "query": query, "maxResults": max_results}
    else:
        url = f"{creds['url']}/rest/api/3/user/search"
        params = {"query": query, "maxResults": max_results}
    response = requests.get(url, params=params, headers=build_headers(), auth=get_auth())
    response.raise_for_status()
    return response.json()
