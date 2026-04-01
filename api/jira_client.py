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

def _create_basic_issue(project_key: str, issue_type: str, summary: str, description: str, assignee_id: str = None, extra_fields: dict = None):
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
        
    if extra_fields:
        fields.update(extra_fields)
        
    payload = {"fields": fields}
    
    response = requests.post(url, json=payload, headers=build_headers(), auth=get_auth())
    response.raise_for_status()
    return response.json()

def create_bug(project_key: str, summary: str, description: str, assignee_id: str = None, observed_in: str = None):
    creds = get_jira_credentials()
    extra_fields = {}
    if observed_in and creds.get("observed_in_field_id"):
        extra_fields[creds["observed_in_field_id"]] = {"value": observed_in}
    return _create_basic_issue(project_key, "Bug", summary, description, assignee_id, extra_fields)

def create_story(project_key: str, summary: str, description: str, assignee_id: str = None):
    return _create_basic_issue(project_key, "Story", summary, description, assignee_id)

def create_task(project_key: str, summary: str, description: str, assignee_id: str = None):
    return _create_basic_issue(project_key, "Task", summary, description, assignee_id)

def create_epic(project_key: str, summary: str, description: str, assignee_id: str = None):
    return _create_basic_issue(project_key, "Epic", summary, description, assignee_id)

def get_issue(issue_key: str):
    creds = get_jira_credentials()
    url = f"{creds['url']}/rest/api/3/issue/{issue_key}"
    headers = {"Accept": "application/json"}
    
    response = requests.get(url, headers=headers, auth=get_auth())
    response.raise_for_status()
    return response.json()

def search_issues(jql: str, max_results: int = 10):
    creds = get_jira_credentials()
    url = f"{creds['url']}/rest/api/3/search"
    
    payload = {
        "jql": jql,
        "maxResults": max_results,
        "fields": ["summary", "status", "assignee", "priority", "created"]
    }
    
    response = requests.post(url, json=payload, headers=build_headers(), auth=get_auth())
    response.raise_for_status()
    return response.json()

def update_issue(issue_key: str, summary: str = None, description: str = None):
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
        
    if not fields:
        raise ValueError("No fields to update. Please provide summary or description.")
        
    payload = {"fields": fields}
    
    response = requests.put(url, json=payload, headers=build_headers(), auth=get_auth())
    response.raise_for_status()
    if response.status_code == 204:
        return {"success": True}
    return response.json() if response.text else {"success": True}

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
