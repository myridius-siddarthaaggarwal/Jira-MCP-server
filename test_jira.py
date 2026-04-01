import os
import json

def run_test():
    # Make sure you set these environment variables before running this script!
    
    # Or, uncomment the lines below and hardcode them just for testing (but DO NOT commit them!):
    # os.environ["JIRA_BASE_URL"] = "https://your-domain.atlassian.net"
    # os.environ["JIRA_EMAIL"] = "your.email@company.com"
    # os.environ["JIRA_API_TOKEN"] = "YOUR-GENERATED-API-TOKEN"

    print("Checking environment variables...")
    if not all([os.environ.get("JIRA_BASE_URL"), os.environ.get("JIRA_EMAIL"), os.environ.get("JIRA_API_TOKEN")]):
        print("❌ Error: Missing environment variables.")
        print("Please set JIRA_BASE_URL, JIRA_EMAIL, and JIRA_API_TOKEN before running the test.")
        return

    print("Environment variables found. Attempting to create a test bug...")
    
    # Replace 'PROJ' with an actual Project Key from your Jira instance
    project_key = input("Enter your Jira Project Key (e.g., PROJ): ").strip().upper()
    if not project_key:
        print("Project Key is required!")
        return
        
    assignee_id = input("Enter Assignee Account ID: ").strip()
    observed_in = input("Enter 'Observed In' custom field value: ").strip()
        
    summary = "Test Bug from MCP Server (Refactored)"
    description = "This is a test bug created to verify that the Jira MCP server connection is working correctly."
    
    from api.jira_client import create_bug
    
    try:
        # Call the api function directly
        result = create_bug(
            project_key=project_key,
            summary=summary,
            description=description,
            assignee_id=assignee_id,
            observed_in=observed_in
        )
        
        print("\n✅ SUCCESS!")
        print(f"Issue Data:")
        print(json.dumps(result, indent=2))
        
        issue_key = result.get('key')
        base_url = os.environ.get("JIRA_BASE_URL", "").rstrip('/')
        print(f"\nYou should see your new ticket here: {base_url}/browse/{issue_key}")
    except Exception as e:
        print("\n❌ FAILED!")
        print(f"Error Message: {str(e)}")

if __name__ == "__main__":
    run_test()
