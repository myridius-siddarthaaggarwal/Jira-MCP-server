import os

def check_jira_credentials():
    url = os.environ.get("JIRA_BASE_URL")
    email = os.environ.get("JIRA_EMAIL")
    token = os.environ.get("JIRA_API_TOKEN")
    
    if not all([url, email, token]):
        return False, "Missing Jira credentials. Please set JIRA_BASE_URL, JIRA_EMAIL, and JIRA_API_TOKEN environment variables."
    return True, ""

def get_jira_credentials():
    base_url = os.environ.get("JIRA_BASE_URL", "")
    return {
        "url": base_url.rstrip('/') if base_url else "",
        "email": os.environ.get("JIRA_EMAIL"),
        "token": os.environ.get("JIRA_API_TOKEN"),
        "observed_in_field_id": os.environ.get("JIRA_OBSERVED_IN_FIELD_ID", "customfield_10097")
    }
